# S2_5th meeting minutes with host

## Meeting Overview:

- Date and Time: Tuesday, October 1, 2023, 10:00 AM
- Duration: Approximately 60 minutes
- Attendees: Rick Doblanovic, Dr Vamsi Madasu, Pengjiabei TANG, Cheng (Chris) Qian, Junheng Yu, Xuan JI (Yufong absent)
- Purpose: Discuss data generation progress, determine next steps, address issues, and set deadlines

## Key Discussion Points:

### Data Generation Progress and Guidance

- Current Status: Team members independently generated different datasets, ranging from 500 to 1100 rows
- Main Challenges: Feature generation, label assignment, attrition rate discrepancies, data authenticity
- Key Guidance from Dr Vamsi Madasu:
  1. Dataset Unification: Emphasized the need for a unified master dataset, targeting about 2000 rows
  2. Feature Generation Method:
     - Using Kaggle dataset as a foundation is a good start
     - For missing features, suggested generating in batches (5 features at a time), gradually understanding and applying correlations
     - Warned against over-relying on labels to generate other features, as this may lead to data bias
  3. Label Generation: Advised randomly assigning labels after generating all features to avoid data manipulation
  4. Data Splitting: Recommended an 80-20 train-test split, emphasizing the importance of the test set
  5. Attrition Rate: Suggested maintaining real-world attrition rates (2-12%), even if this might make prediction challenging
- Conclusion: Generated data needs to balance randomness and real-world relationships, avoiding over-manipulation that leads to false accuracy

### Algorithm Application

- Discussed whether to apply the 5 algorithms from last semester or try new ones
- Dr Vamsi Madasu's recommendation: Prioritize last semester's 5 algorithms, attempt new ones if time permits

### Project Timeline

- Confirmed key dates: October 18 for presentation, October 28 for written report
- Rick and Vamsi emphasized time urgency, advised accelerating progress

### Dashboard Presentation

- Rick reminded that the ultimate goal is to visualize data on a dashboard

## Key Decisions:

- Create a unified master dataset of 2000 rows
- Adopt weekly meetings to accelerate project progress
- Prioritize using the 5 algorithms from last semester

## Action Items:

- All members: Merge datasets, create unified master dataset (Deadline: October 6)
- All members: Determine train-test split method (Deadline: October 6)
- All members: Decide on algorithms to use (Deadline: October 6)
- Pengjiabei TANG: Send invitations for the next two meetings

## Next Steps:

- Next meeting: Friday, October 6, 2023, at 9:30 AM
- Following meeting: Friday, October 13, 2023, at 9:30 AM (tentative)
- Discuss presentation and report support needs in the next meeting

## Additional Notes:

- Emphasized the importance of full team participation
- Rick and Vamsi expressed willingness to support the team's presentation
- Project progress is slightly behind schedule, but the team is confident in meeting deadlines

