This is a simplification of Touhou or a bullet hell game in general for RL Learning
This is still a WIP. Maybe an easy-to-use version will come.

To see or play the game, just do the following:
1. Install `uv`
2. Go to `Pyhou` folder
3. To run the game, run `uv run main.py`. The toml file should handle the requirements.
4. If there's an error from the requirements, just instyall them using `uv sync`

To train the game and see some RL stuff
1. Go to `Pyhou_gym` folder.
2. Run `uv run train.py` to train the model. A zip should appear that can be used to run a modle. You can specify the reward. (Comprehensive reward dict WIP)
3. If you got requirement error, run `uv sync` to install them right away.
4. Run `uv run test.py` to see the agent play by itself.

There's this weird error from Stable Baselines 3 that requires you to have MSVC. YOu should install them if you got error mentioning DLL.
