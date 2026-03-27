import math

class Action:
    def __init__(self, action_data):
        self.steps = action_data.get("steps", [])
        self.current_step = 0
        self.step_timer = 0
        self.completed = False

    def update(self, enemy, player_pos):
        if self.completed:
            return
        
        if self.current_step >= len(self.steps):
            self.current_step = 0
            return
        
        step = self.steps[self.current_step]
        duration = step.get("duration", 1)
        
        self.execute_step(enemy, step, player_pos)
        self.step_timer += 1

        if self.step_timer >= duration:
            self.step_timer = 0
            self.current_step += 1

    # Execute step
    def execute_step(self, enemy, step, player_pos):
        action_type = step.get("type", "wait")

        match action_type:
            case "shoot":
                enemy.shoot(step, player_pos)
            case "wait":
                pass
            case "move":
                enemy.update_pos(step)
            case "teleport": #Not yet
                pass
