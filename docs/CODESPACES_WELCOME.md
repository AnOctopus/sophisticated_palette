# 🎈 Streamlit App Testing Framework 🎈

👋 **Welcome to the Streamlit app testing framework quickstart!** These instructions are optimized
for users who have opened this repo in Github Codespaces as a quickstart view. Follow the instructions
below to get a quick overview of the new framework.

## Instructions

1. A few seconds after opening the codespace, you should see the Sophisticated Palette app open in a "Simple Browser" tab to the right of these instructions.
1. Click around the app to get familiar with the functionality.
1. For a closer look, view the app source code in `app.py`. It should be available in a tab next to this one.
1. This app has tests implemented in `test_app.py`. Review the tests to see examples of the testing framework in action.
1. Finally, you should see a terminal open below these instructions. Click into the terminal and enter `pytest -vv` to execute the tests.
1. Try editing the tests or editing the app to see failures, additional previews, or you can add your own tests.

## Troubleshooting

If you opened the Codespace and the app never opened after a few minutes, you can run the setup commands manually

```sh
pip3 install --user -r requirements.txt
streamlit run app.py > /dev/null 2>&1 &
pytest
```

## Next steps

Hopefully this is a helpful overview of the feature! A few resources to explore next:

- View the [full README](./README.md) for this repo, including local and CI setup
- [Detailed documentation](https://docs.google.com/document/d/1Qscb-Ux8hEPo9hdoIjEw666wmzXO_u0JmpYo-4X6kSw/preview) - preview install instructions and API reference
- [Add feedback here](https://discuss.streamlit.io/t/feedback-wanted-for-streamlit-app-testing/52861)
