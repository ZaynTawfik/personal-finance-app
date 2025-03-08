    # Transactions Analysis Page
    elif page == "Transactions Analysis":
        st.header("Transactions Analysis")
        csv_tool = FileReadTool(file_path='./transactions.csv')
        #uploaded_file = st.file_uploader("Upload Transactions CSV", type=["csv"])
        
        if csv_tool:
            #transactions = pd.read_csv(uploaded_file)
            #st.session_state.transactions = transactions
            
            financial_analysis_agent = Agent(config=agents_config['financial_analysis_agent'],tools=[csv_tool])
            budget_planning_agent = Agent(config=agents_config['budget_planning_agent'],tools=[csv_tool])
            financial_viz_agent = Agent(config=agents_config['financial_viz_agent'],allow_code_execution=False)

            # Create tasks
            expense_analysis = Task(
              config=tasks_config['expense_analysis'],
              agent=financial_analysis_agent
            )

            budget_management = Task(
              config=tasks_config['budget_management'],
              agent=budget_planning_agent
            )

            financial_visualization = Task(
              config=tasks_config['financial_visualization'],
              agent=financial_viz_agent
            )

            final_report_assembly = Task(
              config=tasks_config['final_report_assembly'],
              agent=budget_planning_agent,
              context=[expense_analysis, budget_management, financial_visualization]
            )

            #Create crew
            finance_crew = Crew(
              agents=[
                financial_analysis_agent,
                budget_planning_agent,
                financial_viz_agent
              ],
              tasks=[
                expense_analysis,
                budget_management,
                financial_visualization,
                final_report_assembly
              ],
              verbose=True
            )

            result = finance_crew.kickoff()
            st.session_state.analysis_result = result
            
            st.subheader("Spending Analysis")
            st.write(result.raw)
