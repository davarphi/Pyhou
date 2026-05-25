This is a simplification of Touhou or a bullet hell game in general for RL Learning
This is still a WIP.

To see or play the game, just do the following:
1. Install `uv`
2. Go to `Pyhou` folder
3. To run the game, run `uv run main.py`. The toml file should handle the requirements.
4. If there's an error from the requirements, just instyall them using `uv sync`

To train the game and see some RL stuff
1. Go to `Pyhou_gym` folder.
2. Run `uv run train.py` to train the model. A zip should appear that can be used to run a model. You can specify the reward.
3. If you got requirement error, run `uv sync` to install them right away.
4. Run `uv run test.py` to see the agent play by itself.

There's this weird error from Stable Baselines 3 that requires you to have MSVC. YOu should install them if you got error mentioning DLL.

The reward for now : 

* time_penalty = penalty for each frame the agent still playing.
* enemy_hit = reward for each hit to enemy.
* player_hit = penalty to each player hit.
* aligned_pos = reward for being in a position where you can shoot the enemy.
* win = reward for each win.
* loss = reward for each loss. this is when the player touches the enemy.

train.py have several args you can use

* --pattern (name).json : run (name).json file to train. Defaults to test_attack.json
* --save (name) : save the training model to (name).zip. Defaults to pyhou

test.py also have several args you can use

* --pattern (name).json : run (name).json file to test. Defaults to test_attack.json
* --model (name) : use the trained model to play with. Defaults to pyhou


Best for now : reward = {
    "time_penalty": -0.01,
    "enemy_hit": 8,
    "player_hit": -32,
    "aligned_pos": 4,
    "win":50,
    "loss":-200
}, frame_skip 10, train > 100000

reward = {
    "time_penalty": -0.001,
    "enemy_hit": 8,
    "player_hit": -40,
    "aligned_pos": 12,
    "win":50,
    "loss":-200
} training 500000

Best stats (for now): 

Health : 0.0
Bullets that hit player : 8
Bullets that hit enemy : 100
Time : 24.284

test_attack.json can be done optimally humanly by just going to the bottom and strafe.
