# Cornershop's Backend Test - David Salvatierra Explanation

In this README file I explain my solution to the test

## Assumptions

- In order to get the solution I created some extra views and functionalities
- The test speak of Nora as the only user to be able to see some functionalities, I added some users for testing purposes and also some validations and functions are thought to leave ready to add more Nora's type user (supervisors)
- All the implementation of the solution was created and tested in local development settings and enviroments for costs and time reasons, so I missing configurations for uploading the solution to a more production kind enviroment (like using other database or uploading to AWS)
- The tests cover some portions of thes views created and mostly are simples cases but also look for validate possile errors and intended functionality
- I use Celery and Redis to create the async function to send the slack reminder, I tested with my own slack enviroment/team and I add a field to the Employee Model to have the slack personal id (slack_id) in order to know to whom send the reminder and if is missing fail silently, all this using offical python slack client and my personal token
- All enviroment variables are saved .env that vscode provide, so when you make testing you need to replace it with the your own enviroment variables values
- All the tests cases are unit test type, I miss by time making E2E test cases, for example using selenium
- For the visual aspect I use boostrap from 2 python packages (crispy-forms and boostrap4) because it was fast and also because I need to improve my front-end skills
- Most of the code is reviewed and corrected with pylint and pylint-django using pep8 style guide
- I put messages from the django message framework but I have some problems to make it to work all the time in development enviroment when I use redirect, I lacked time to have this working 100%
- I leave a little script to create some users
- I use Pipfile tom manage packages and virtual enviroment
- I think that I can do a lot of stuff better like handling the selection menu in a better way, or rendering the forms in the template better and other stuffs

## Final Thoughts 

I enjoy the test, I want to thank you for the oportunity. It took me longer than I expected but I improve in the process.

I would love to be part of Cornershop!!!
