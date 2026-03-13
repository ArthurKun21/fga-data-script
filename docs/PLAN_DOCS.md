# FGA Data script

This is a set of scripts to be run in order to generate data to be used for the FGA Project. It uses the Atlas Academy API to fetch raw data and turn them into a format that the FGA Project can use.

## Support Template Images

This would be responsible for fetching the raw images to be converted into the support template images used in the FGA Project.

### Support Template Images Workflow

- Fetch the raw images from the Atlas Academy API.
- Copy the output repository to the current repository.
- Copy the json file containing the current progress.
- Process the raw images and generate the support template images.
- Update the json file with the new progress.
- Push the changes to the repository.
