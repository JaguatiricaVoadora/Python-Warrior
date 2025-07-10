import pygame
import os

class PlayerAnimations:
    def __init__(self, sprite_dir):
        self.run_frames = self.load_frames(os.path.join(sprite_dir, 'Run_frames'), 10)
        self.idle_frames = self.load_frames(os.path.join(sprite_dir, 'Idle_frames'), 10)
        self.jump_frames = self.load_frames(os.path.join(sprite_dir, 'Jump_frames'), 3)
        self.fall_frames = self.load_frames(os.path.join(sprite_dir, 'Fall_frames'), 3)
        self.roll_frames = self.load_frames_dynamic(os.path.join(sprite_dir, 'Roll_frames'))

        self.run_frame_index = 0
        self.run_anim_speed = 0.25
        self.run_anim_counter = 0
        self.idle_frame_index = 0
        self.idle_anim_speed = 0.10
        self.idle_anim_counter = 0
        self.jump_frame_index = 0
        self.jump_anim_speed = 0.10
        self.jump_anim_counter = 0
        self.fall_frame_index = 0
        self.fall_anim_speed = 0.10
        self.fall_anim_counter = 0
        self.roll_frame_index = 0
        self.roll_anim_speed = 0.20
        self.roll_anim_counter = 0

    def load_frames(self, folder, count):
        frames = []
        for i in range(count):
            frame_path = os.path.join(folder, f'frame_{i:03}.png')
            if os.path.exists(frame_path):
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (180, 200))
                frames.append(frame)
        return frames

    def load_frames_dynamic(self, folder):
        frames = []
        if os.path.exists(folder):
            frame_files = sorted([f for f in os.listdir(folder) if f.endswith('.png')])
            for frame_file in frame_files:
                frame_path = os.path.join(folder, frame_file)
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (180, 200))
                frames.append(frame)
        return frames

    def update(self, state, moving, on_ground, player_vel_y, is_rolling):
        # state: 'idle', 'run', 'jump', 'fall', 'roll'
        if is_rolling:
            self.roll_anim_counter += self.roll_anim_speed
            if self.roll_anim_counter >= 1:
                self.roll_frame_index += 1
                self.roll_anim_counter = 0
                if self.roll_frame_index >= len(self.roll_frames):
                    self.roll_frame_index = len(self.roll_frames) - 1
        elif not on_ground:
            if player_vel_y > 0:
                self.fall_anim_counter += self.fall_anim_speed
                if self.fall_anim_counter >= 1:
                    self.fall_frame_index = (self.fall_frame_index + 1) % len(self.fall_frames)
                    self.fall_anim_counter = 0
            else:
                self.jump_anim_counter += self.jump_anim_speed
                if self.jump_anim_counter >= 1:
                    self.jump_frame_index = (self.jump_frame_index + 1) % len(self.jump_frames)
                    self.jump_anim_counter = 0
        elif moving:
            self.run_anim_counter += self.run_anim_speed
            if self.run_anim_counter >= 1:
                self.run_frame_index = (self.run_frame_index + 1) % len(self.run_frames)
                self.run_anim_counter = 0
        else:
            self.idle_anim_counter += self.idle_anim_speed
            if self.idle_anim_counter >= 1:
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_frames)
                self.idle_anim_counter = 0

    def get_frame(self, state, is_rolling, player_vel_y, on_ground, moving):
        if is_rolling and self.roll_frames:
            return self.roll_frames[self.roll_frame_index]
        elif not on_ground:
            if player_vel_y > 0:
                return self.fall_frames[self.fall_frame_index]
            else:
                return self.jump_frames[self.jump_frame_index]
        elif moving:
            return self.run_frames[self.run_frame_index]
        else:
            return self.idle_frames[self.idle_frame_index]

    def reset_roll(self):
        self.roll_frame_index = 0
        self.roll_anim_counter = 0
