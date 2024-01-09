from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from robot.api import SuiteVisitor, TestSuite

class TestExecutionView(APIView):
    def post(self, request):
        tests = request.data['tests']
        test_steps = tests[0]['steps']  # Assuming a single test for now

        robot_test_case = '\n'.join(test_steps)  # Create test case string
        suite = TestSuite('Dynamic Test Suite')
        suite.tests.create('Test Case', robot_test_case)

        result = suite.run(output='output.xml')  # Execute test

        # Process and format test results
        visitor = TestResultVisitor()
        result.visit(visitor)
        test_output = visitor.get_formatted_output()
        return Response({'output': test_output})
    
class TestResultVisitor(SuiteVisitor):
    def __init__(self):
        self.output = ''

    def visit_test(self, test):
        self.output += f"Test: {test.name}\n"
        for keyword in test.keywords:
            self.output += f"- {keyword.name}: {keyword.status}\n"