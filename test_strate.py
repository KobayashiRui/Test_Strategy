import rcl
import math
import kid.goal
import kid.motion
import kid.action.approach
import actionbase.search
import tools.geometry
import tools.algorithm
import time
from tools.decorator import classproperty

class KickBall(rcl.Action):
    def do_process(self, player):
        while True:
            print("shoot !")
            player.motion.cancel()
            player.wait_until_status_updated()
            player.sleep(2.0)
            player.__agent.effector.play_motion(rcl.SoccerAgent.Effector.KICK_R)
            player.motion.cancel()
            player.start_memorize_kickball()
            player.wait_until_motion_finished()
            yield

    def apply_behavior(self, world_state):
        return world_state

    def get_cost(self, world_state):
        return 5

    def get_precondition(self):
        return [(rcl.WorldState.K_HAVE_BALL, True)]

    def get_deletion_list(self):
        return []

    def get_additional_list(self):
        return [(rcl.WorldState.K_BALL_IN_TARGET, True)]

#        prev_autolocalization = player.get_auto_localization_mode()
#        player.set_auto_localization_mode(0)
#        player.start_memoriza_observation()
#        num_found_landmarks = 0
#        search_pan_angles = [-120,0,120]
#
#        try:
#            for pan in search_pan_angles:
#                player.wait_until_status_updated()
#                player.__agent.effector.set_pan_deg(pan)
#            ballarr_lc = player.world.get_estimatd_object_pos_lc(rcl.SoccerAgent.Brain.BALL)
#
#            if ballarr_lc:
#                player.__agent.effector.set_pan_deg(rcl.tools.geometry.direction_deg(ballarr_lc[0]))
#        finally:
#            player.set_auto_localization_mode(prev_autolocalization)
class Approach_Ball(rcl.Action):
    def __init__(self):
        rcl.Action.__init__(self)
    def do_process(self, player):
        while True:
            target_pos_lc = player.world.get_estimated_object_pos_lc(rcl.SoccerAgent.Brain.BALL)
            target_dist_lc = tools.geometry.distance(target_pos_lc[0])
            target_direction_deg = tools.geometry.direction_deg(target_pos_lc[0])
            if math.fabs(target_direction_deg) > 30:
                walk_th = tools.algorithm.clamp(target_direciton_deg, 10, -10)
                player.motin.move(0, walk_th, 0, 12, 0)
            elif math.fabs(target_dist_lc) > 200:
                player.motion.move(0, 16, 0, 0)
            yield

    def apply_behavior(self, world_state):
        return world_state

    def get_cost(self, world_state):
        return 5

    def get_precondition(self):
        return [(rcl.WorldState.K_KNOW_BALL_POS, True)]

    def get_deletion_list(self):
        return [(rcl.WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, False)]
        
    def get_additional_list(self):
        return [(rcl.WorldState.K_HAVE_BALL, True)]


class Serch_Ball(rcl.Action):
    def __init__(self):
        rcl.Action.__init__(self)
        self.finish_time = None

    def do_process(self, player):
        player.motion.cancel()
        player.motion.turn_neck(0)
        player.wait_until_status_updated()
        try:
            while True:
                ballarr_lc = player.world.get_estimated_object_pos_lc(rcl.SoccerAgent.Brain.BALL)
                if ballarr_lc:
                    player.motion.turn_neck(rcl.tools.geometry.direction_deg(ballarr_lc[0]))
                    yield
        finally:
            player.set_auto_localization_mode(1)

    def get_precondition(self):
        return []

    def get_deletion_list(self):
        return []

    def get_additional_list(self):
        return [(rcl.WorldState.K_KNOW_BALL_POS, True)]

    def apply_behavior(self, world_state):
        return world_state

    def get_cost(self, world_state):
        return 6


class Idling(rcl.Action):
    def do_process(self, player):
        player.motion.cancel()
        try:
            while True:
                player.forget_ball_memory()
                player.sleep(1)
                yield
        finally:
            player.set_selfpos((2000,0,0))

    def get_precondition(self):
        return []

    def get_deletion_list(self):
        return []

    def get_additional_list(self):
        return [(rcl.WorldState.K_IDLE, True)]

    def apply_behavior(self, world_state):
        return world_state

    def get_cost(self, world_state):
        return 0


class TutoRole(rcl.SoccerRole):
    def __init__(self, id_):
        conf_file = "kid/actionconf/kid-strategy.cnf"
        rcl.SoccerRole.__init__(self, id_, conf_file)

    def _get_updated_home_pos_gl(self, world_state):
        return None

    def _get_updated_goal_pos_gl(self, world_state):
        return [(5000, 0, 0)]

    def _get_updated_goal(self, world_state):
        if player.world.switch_state.state(rcl.SoccerAgent.Brain.SWITCH_3):
            return kid.goal.idling
        else:
            return kid.goal.ball_in_goal

    def _get_updated_action_list(self):
        if not self.action_list:
            action_list = [
                Approach_Ball(),
                Idling(),
                KickBall(),
                Serch_Ball(),
            ]
        else:
            action_list = self.action_list
        
        return action_list


class Tuto_Strategy(rcl.Strategy):
    def __init__(self):
        rcl.Strategy.__init__(self)

        self.__goal_cls = kid.goal.idling
        self.__role_cls = TutoRole(1)
        self.__common_string = ""

    @property
    def goal_symbol_list(self):
        return self.__goal_symbol_list

    @property
    def symbol_dict(self):
        return self.__role_cls.symbol_dict

    @property
    def action_list(self):
        return self.__role_cls.action_list

    @property
    def common_string(self):
        return self.__common_string

    @property
    def get_target_arrpos_gl(self):
        return self.__target_arrpos_gl

    def update(self, world_state):
        old_goal_cls = self.__goal_cls
        assert not None in (self.__goal_cls, self.__role_cls), "Not Assigned strategic property"
        
        self.__role_cls.update(world_state)
        
        self.__target_arrpos_gl = self.__role_cls._get_updated_goal_pos_gl(world_state)
        self.__goal_cls = self.__role_cls.goal
        self.__goal_symbol_list = self.__goal_cls.get_goal_state()
        
        if old_goal_cls is not self.__goal_cls:
            print "goal changed: %s -> %s" % (old_goal_cls.__class__.__name__, self.__goal_cls.__class__.__name__)
            changed = True
        else:
            changed = False

        return changed


    def create_field_properties(self):
        class HLKidFieldProperties(rcl.StaticFieldProperties):
            @classproperty
            def ENEMY_GOAL_POLE_GL(cls):
                return [(4500, 750, 0), (4500, -750, 0)]
            
            @classproperty
            def OUR_GOAL_POLE_GL(cls):
                return [(-4500, -750, 0), (-4500, 750, 0)]
            
            @classproperty
            def ENEMY_GOAL_GL(cls):
                return (5000, 0, 0)
            
            @classproperty
            def OUR_GOAL_GL(cls):
                return (-5000, 0, 0)
            
            @classproperty
            def NUM_PLAYERS(cls):
                return 6
        
        return HLKidFieldProperties()

    def create_motion(self, effector):
        return kid.motion.HR46Motion(effector)

if __name__ == '__main__':
    player = rcl.SoccerPlayer(lambda : Tuto_Strategy())
    
    try:
        player.run()
    except Exception, e:
        player.debug_log_ln("Exception: "+ str(e))
        time.sleep(1)
        player.terminate()
        time.sleep(1)
        raise
    except (KeyboardInterrupt, SystemExit):
        player.terminate()
        raise
