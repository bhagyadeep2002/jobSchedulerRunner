## Job Scheduler Runner

A job scheduler and runner similar to AWS Lambda + Eventbridge where user can login and basically post a piece of code that will be executed using the designated cron job (current implementation).

## Todo

- [x] Implement Auth
- [x] Implement Jobs DB
- [x] Implement Jobs Endpoints
- [X] Get code in payload and store it in python file with unique name and store that name in db
- [X] Implement actual Job execution
- [ ] Move next run schedule from DB to separate file
- [ ] Create dockerfile for deployment
- [ ] Fix state changes for job run (currently straight away goes to completed)

...... and much more!
