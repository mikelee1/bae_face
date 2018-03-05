# -*- coding: utf-8 -*-
def to_response(data):
    return {
        'error_code': 0x0000,
        'response_data': data
    }

def to_response_withpageid(data,currentid):
    return {
        'error_code': 0x0000,
        'currentid':currentid,
        'response_data': data
    }

def to_error(code, message):
    return {
        'error_code': code,
        'error_message': message
    }


# Default 0x000x
DEFAULT = to_response(None)

# General 0x001x
ILLEGAL_REQUEST_PARAMETERS = to_error(0x0010, 'illegal request parameters')
REQUEST_TOO_OFTEN = to_error(0x0011, 'request too often')

# Authentication 0x002x
USER_INACTIVE = to_error(0x0020, 'user is inactive')
USER_NOT_EXIST_OR_WRONG_PASSWORD = to_error(0x0021, 'user does not exist or wrong password')

# User 0x003x
USERNAME_ALREADY_EXISTS = to_error(0x0030, 'username already exists')
EMAIL_ALREADY_EXISTS = to_error(0x0031, 'email already exists')
SEND_MAIL_FAILED = to_error(0x0032, 'send mail failed')
CURRENT_PASSWORD_WRONG = to_error(0x0033, 'current password is incorrect')
AUTH_CODE_EXPIRED = to_error(0x0034, 'authentication code is expired')

# Notice 0x004x
NOTICE_NOT_EXIST = to_error(0x0040, 'notice does not exist')

# Task 0x005x
CHOICE_QUESTION_NOT_EXIST = to_error(0x0050, 'choice question does not exist')
TASK_NOT_EXIST = to_error(0x0051, 'task does not exist')

# Score 0x006x
ALREADY_SUBMITTED = to_error(0x0060, 'choice is already submitted')
WRITE_UP_TYPE_ERROR = to_error(0x0061, 'write_up_type_error')

# Team 0x007x
TEAMNAME_ALREADY_EXIST = to_error(0x0070, 'teamname already exist')
USE_HAS_JOIN_OTHER = to_error(0x0071, 'user has join other team')
DONT_JOIN_THIS_TEAM = to_error(0x0072, 'do not join this team')
TEAM_NOT_EXIST = to_error(0x0073, 'team do not exist')
USE_HAS_NO_TEAM = to_error(0x0074, 'user has no team')
USE_NOT_EXIST= to_error(0x0075, 'user not exist')

# Contest 0x01xx
CONTEST_END = to_error(0x0101, 'contest has end')
CONTEST_PLAYING = to_error(0x0102, 'contest is playing')
HAVE_ENROLED = to_error(0x0103, 'has enrol this contest')
ENROL_TIME_NOT_BEGIN = to_error(0x0104, 'enrol time not begin')
ENROL_TIME_OVER = to_error(0x0105, 'enrol time over')
TEAM_HAS_SUBMIT_TASK = to_error(0x0106, 'team has submit this task')
NO_PERM_FOR_TASK = to_error(0x0107, 'no permission for task')
ENROL_ONLY_TEAMLEADER = to_error(0x0108, 'only teamleader can enrol')
CONTEST_NOT_START = to_error(0x0109, 'contest is not start')
TEAM_FORBIDDEN = to_error(0x010a, 'team forbidden')
TEAM_NOT_ENROL_CONTEST = to_error(0x010b, 'team not enrol contest')
CONTEST_PAUSE = to_error(0x010c, 'contest pause')
CONTEST_DONT_SHOW_RANK = to_error(0x010d, 'contest dont show rank')


# =================================
TEAM_STATUS_NOMAL = 0
TEAM_STATUS_DEL = 1
TEAM_STATUS_FIRE = 2

TEAM_USER_INVITE = 0
TEAM_USER_JOIN = 1
TEAM_USER_REFUSE = 2
TEAM_USER_EXIT = 3
TEAM_USER_NEED_JOIN = 4
TEAM_USER_DELETE = 5

TEAM_APPL_REFUSE = 1
TEAM_APPL_ACCEPT = 0

STATUS_NOMAL = 0
STATUE_DEL = 1

CONTEST_STATUS_PAUSE = 2       #比赛暂停
CONTEST_TEAM_FORBIDDEN = 1     #队伍禁止比赛

CONTEST_TYPE_CG = 0     #闯关型
CONTEST_TYPE_NCG = 1    #解题型
CONTEST_TYPE_SHARE = 2  #分享型
