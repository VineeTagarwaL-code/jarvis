import json
import openai
import time
from config import OPENAI_API_KEY, OPENAI_SETTINGS, SYSTEM_PROMPT
from tools import FUNCTIONS, FUNCTION_MAP
from conversation_manager import ConversationManager

class AIHandler:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.conversation_manager = ConversationManager()
    
    def process_query(self, query):
        """Process a user query and return the appropriate response."""
        try:
            print("Thinking...")
            
            # Check if autonomous mode should be used
            if self.conversation_manager.should_use_autonomous_mode(query):
                return self._process_autonomous_query(query)
            else:
                return self._process_single_query(query)
                
        except Exception as e:
            print(f"Error in AI processing: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _process_single_query(self, query):
        """Process a single query with context."""
        # Get conversation context
        context_messages = self.conversation_manager.get_context_messages()
        
        # Build messages with context
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(context_messages)
        messages.append({"role": "user", "content": query})
        
        response = self.client.chat.completions.create(
            model=OPENAI_SETTINGS['model'],
            messages=messages,
            functions=FUNCTIONS,
            function_call="auto",
            max_tokens=OPENAI_SETTINGS['max_tokens'],
            temperature=OPENAI_SETTINGS['temperature']
        )
        
        choice = response.choices[0]
        tool_calls = []
        
        # Handle function calls
        if choice.finish_reason == "function_call":
            tool_result = self._execute_function(choice.message.function_call)
            tool_calls.append({
                'function': choice.message.function_call.name,
                'arguments': choice.message.function_call.arguments,
                'result': tool_result
            })
            # Feed tool result back to OpenAI for refinement
            final_response = self._refine_tool_response(query, tool_result)
        else:
            final_response = choice.message.content
        
        # Add to conversation history
        self.conversation_manager.add_interaction(query, final_response, tool_calls)
        
        return final_response
    
    def _process_autonomous_query(self, query):
        """Process a complex query with autonomous multi-tool execution."""
        print("Autonomous mode: Planning complex task...")
        
        # Step 1: Create a plan
        plan = self._create_execution_plan(query)
        print(f"Plan: {plan}")
        
        # Step 2: Execute the plan with redundancy prevention
        results = []
        tool_calls = []
        executed_functions = set()  # Track executed functions to prevent redundancy
        
        try:
            # Execute multiple tool calls based on the plan
            for i in range(self.conversation_manager.max_tool_calls):
                print(f"Autonomous execution step {i+1}...")
                
                # Get next action from AI
                next_action = self._get_next_action(query, results, plan, executed_functions)
                
                if not next_action or next_action.get('action') == 'complete':
                    print("Autonomous execution completed.")
                    break
                
                # Execute the action
                if next_action.get('function_call'):
                    function_name = next_action['function_call'].name
                    function_args = json.loads(next_action['function_call'].arguments)
                    
                    # Check for redundancy
                    if self._is_redundant_call(function_name, function_args, executed_functions):
                        print(f"Skipping redundant call to {function_name}")
                        continue
                    
                    tool_result = self._execute_function(next_action['function_call'])
                    results.append(tool_result)
                    tool_calls.append({
                        'function': function_name,
                        'arguments': next_action['function_call'].arguments,
                        'result': tool_result
                    })
                    
                    # Mark function as executed
                    executed_functions.add(function_name)
                    print(f"Executed: {function_name}")
                
                # Small delay between actions
                time.sleep(0.5)
            
            # Step 3: Generate final response
            final_response = self._generate_final_response(query, results, plan)
            
        except Exception as e:
            final_response = f"Autonomous execution encountered an error: {str(e)}"
        
        # Add to conversation history
        self.conversation_manager.add_interaction(query, final_response, tool_calls)
        
        return final_response
    
    def _is_redundant_call(self, function_name, function_args, executed_functions):
        """Check if a function call is redundant."""
        # If function was already executed, it's redundant
        if function_name in executed_functions:
            return True
        
        # For web data calls, check if similar queries were already made
        if function_name == "get_web_data":
            query = function_args.get("query", "").lower()
            # Check if we already have web data results that could answer this
            # This is a simple check - in production you might want more sophisticated similarity detection
            if "stock" in query and any("stock" in str(result).lower() for result in self.conversation_manager.conversation_history[-3:]):
                return True
        
        return False
    
    def _create_execution_plan(self, query):
        """Create an execution plan for complex tasks."""
        planning_prompt = f"""
        Task: {query}
        
        Available tools:
        - get_web_data: Search the web for information (web scraping)
        - open_any_url: Open a website in browser
        - open_application: Open desktop applications
        - get_system_stats: Get computer system information
        - take_screenshot: Capture screen
        - get_current_time: Get current time
        - simple_calculator: Perform calculations
        
        Create a concise, efficient plan with 1-2 steps maximum. Be specific about which tool to use:
        - Use get_web_data for searching/finding information
        - Use open_any_url for opening specific websites
        - Use open_application for launching desktop apps
        
        Avoid suggesting actions that don't match available tools.
        """
        
        response = self.client.chat.completions.create(
            model=OPENAI_SETTINGS['model'],
            messages=[
                {"role": "system", "content": "You are a task planning assistant. Create concise, efficient plans using only the available tools. Be precise about tool names and purposes."},
                {"role": "user", "content": planning_prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def _get_next_action(self, original_query, current_results, plan, executed_functions):
        """Get the next action to execute in autonomous mode."""
        context = f"Original query: {original_query}\nPlan: {plan}\nCurrent results: {current_results}\nExecuted functions: {list(executed_functions)}"
        
        # If we already have results, ask if we should complete
        if current_results:
            context += "\n\nYou already have results. Consider if the task is complete or if one more action is needed."
        
        response = self.client.chat.completions.create(
            model=OPENAI_SETTINGS['model'],
            messages=[
                {"role": "system", "content": "You are an autonomous agent. Determine the next action. Avoid redundant calls. If the task seems complete, indicate completion."},
                {"role": "user", "content": f"{context}\n\nWhat should I do next? Provide a function call or indicate completion."}
            ],
            functions=FUNCTIONS,
            function_call="auto",
            max_tokens=200,
            temperature=0.5
        )
        
        choice = response.choices[0]
        
        if choice.finish_reason == "function_call":
            return {
                'action': 'execute',
                'function_call': choice.message.function_call
            }
        else:
            return {
                'action': 'complete',
                'reason': choice.message.content
            }
    
    def _generate_final_response(self, query, results, plan):
        """Generate a final response summarizing all results."""
        if not results:
            return "I couldn't complete the requested task."
        
        # Use the last result as the primary response
        primary_result = results[-1]
        
        summary_prompt = f"""
        Original query: {query}
        Results: {primary_result}
        
        Provide a concise, natural response based on the result.
        Keep it brief and helpful.
        """
        
        response = self.client.chat.completions.create(
            model=OPENAI_SETTINGS['model'],
            messages=[
                {"role": "system", "content": "You are Jarvis. Provide concise, helpful responses."},
                {"role": "user", "content": summary_prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _execute_function(self, function_call):
        """Execute a function call and return the result."""
        fn_name = function_call.name
        arguments = json.loads(function_call.arguments)
        
        print(f"Calling function: {fn_name}")
        
        if fn_name in FUNCTION_MAP:
            try:
                if fn_name == "get_web_data":
                    print(f"Getting web data for: {arguments['query']}")
                
                # Execute the function with arguments
                if fn_name == "get_current_time":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "open_any_url":
                    return FUNCTION_MAP[fn_name](arguments["url"])
                elif fn_name == "simple_calculator":
                    return FUNCTION_MAP[fn_name](arguments["expression"])
                elif fn_name == "get_system_stats":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "take_screenshot":
                    filename = arguments.get("filename")
                    return FUNCTION_MAP[fn_name](filename)
                elif fn_name == "click_position":
                    return FUNCTION_MAP[fn_name](arguments["x"], arguments["y"])
                elif fn_name == "type_text":
                    return FUNCTION_MAP[fn_name](arguments["text"])
                elif fn_name == "press_key":
                    return FUNCTION_MAP[fn_name](arguments["key"])
                elif fn_name == "get_screen_size":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "get_mouse_position":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "scroll":
                    direction = arguments["direction"]
                    amount = arguments.get("amount", 3)
                    return FUNCTION_MAP[fn_name](direction, amount)
                elif fn_name == "close_active_window":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "minimize_window":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "get_running_apps":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "copy_to_clipboard":
                    return FUNCTION_MAP[fn_name](arguments["text"])
                elif fn_name == "get_web_data":
                    return FUNCTION_MAP[fn_name](arguments["query"])
                elif fn_name == "open_system_settings":
                    return FUNCTION_MAP[fn_name](arguments["setting_type"])
                elif fn_name == "change_font_size":
                    action = arguments.get("action", "increase")
                    target_percentage = arguments.get("target_percentage")
                    return FUNCTION_MAP[fn_name](action, target_percentage)
                elif fn_name == "list_voices":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "set_voice":
                    voice_index = arguments.get("voice_index")
                    voice_name = arguments.get("voice_name")
                    return FUNCTION_MAP[fn_name](voice_index=voice_index, voice_name=voice_name)
                elif fn_name == "list_chrome_profiles":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "open_chrome_with_profile":
                    profile_name = arguments.get("profile_name")
                    profile_id = arguments.get("profile_id")
                    return FUNCTION_MAP[fn_name](profile_name=profile_name, profile_id=profile_id)
                elif fn_name == "open_application":
                    app_name = arguments.get("app_name")
                    profile_name = arguments.get("profile_name")
                    return FUNCTION_MAP[fn_name](app_name, profile_name=profile_name)
                else:
                    return "Sorry, I don't know how to execute that function."
                    
            except Exception as e:
                return f"Error executing {fn_name}: {str(e)}"
        else:
            return "Sorry, I don't know how to do that yet."
    
    def _refine_tool_response(self, original_query, tool_result):
        """Take tool result and refine it through OpenAI for better response."""
        try:
            print("Refining response...")
            
            refinement_prompt = f"""
            Original user query: "{original_query}"
            Tool result: "{tool_result}"
            
            Please provide a refined, concise, and natural response based on the tool result. 
            Make it sound like a helpful assistant speaking to the user.
            Keep it as short as possible. between 10 and 20 words.
            Do not include any other text or explanations.

            """
            
            refinement_response = self.client.chat.completions.create(
                model=OPENAI_SETTINGS['model'],
                messages=[
                    {"role": "system", "content": "You are Jarvis, a helpful AI assistant. Provide concise, natural responses based on the given information."},
                    {"role": "user", "content": refinement_prompt}
                ],
                max_tokens=150,  # Shorter for refinement
                temperature=0.7
            )
            
            refined_response = refinement_response.choices[0].message.content
            return refined_response
            
        except Exception as e:
            print(f"Error refining response: {e}")
            # Fall back to original tool result if refinement fails
            return tool_result
    
    def get_conversation_stats(self):
        """Get conversation statistics."""
        return self.conversation_manager.get_execution_stats()
    
    def clear_conversation_history(self):
        """Clear conversation history."""
        self.conversation_manager.clear_history()
        return "Conversation history cleared." 