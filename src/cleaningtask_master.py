#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import roslib
import smach
from enter_room.srv import EnterRoom
from happymimi_navigation.srv import NaviLocation
from happymimi_voice_msgs.srv import TTS, YesNo
from happymimi_manipulation_msgs.srv import RecognitionToGrasping, RecognitionToGraspingRequest
tts_srv = rospy.ServiceProxy('/tts', StrTrg)


class EnterRoom(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes = ['enter_success'])
        self.enter_room = rospy.ServiceProxy('/enter_room_server', EnterRoom)
        self.navi_srv = rospy.ServiceProxy('/navi_location_server', NaviLocation)
        
    def execute(self, userdate):
        self.enter_room(1.0, 0.5)
        self.navi_srv('cml_start')
        tts_srv("Should I grab the bottle")
        return 'enter_success'

class YesNo(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes = ['yes_no_success'])
        self.yesno_srv = rospy.ServiceProxy('/yes_no', YesNo)
        self.grasp_srv = rospy.ServiceProxy('/recognition_to_grasping', RecognitionToGrasping)

    def execute(self):
        answer = self.yesno_srv().result
        if answer:
            self.grasp_result = self.grasp_srv(RecognitionToGraspingRequest(target_name='bottle')).result
            if self.grasp_result == False:
                if grasp_count >= 3: #####
                    self.tts_srv("/fd/grasp_failed")
                    break
                else:
                    self.tts_srv("/fd/grasp_retry")
                grasp_count += 1
            else:
                self.tts_srv('/fd/grasp_success')
                break
            

        else:
            self.grasp_result = self.grasp_srv(RecognitionToGraspingRequest(target_name='cup')).result
            if self.grasp_result == False:
                if grasp_count >= 3: #####
                    self.tts_srv("/fd/grasp_failed")
                    break
                else:
                    self.tts_srv("/fd/grasp_retry")
                grasp_count += 1
            else:
                self.tts_srv('/fd/grasp_success')
                break
        



class Findbin(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes = [''])





class Grasp(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcoms = [''])
