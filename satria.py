# -*- coding: utf-8 -*-
# Edited from script LineVodka script made by Merkremont
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{},
    'ProtectQR':False
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + "Selamat Datang Di " + group.name)
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
				client.kickoutFromGroup(op.param1,[op.param2])
				client.inviteIntoGroup(op.param1,[op.param3])
				sendMessage(op.param1, client.getContact(op.param2).displayName + ", Kicker kampret")				
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_UPDATE_GROUP(op):
    try:
                sendMessage(op.param1, client.getContact(op.param2).displayName + ", Jangan Dimainin QR-nya :3\nSaya Kick ya")
                client.kickoutFromGroup(op.param1,[op.param2])
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_UPDATE_GROUP\n\n")
        return

tracer.addOpInterrupt(11,NOTIFIED_UPDATE_GROUP)

def NOTIFIED_CANCEL_INVITATION_GROUP(op):
    try:
                sendMessage(op.param1, client.getContact(op.param2).displayName + ", Kenapa dibatalin?\nitu temen saya")
                client.kickoutFromGroup(op.param1,[op.param2])
                client.inviteIntoGroup(op.param1,[op.param3])
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_CANCEL_INVITATION_GROUP\n\n")
        return

tracer.addOpInterrupt(32,NOTIFIED_CANCEL_INVITATION_GROUP)

def CANCEL_INVITATION_GROUP(op):
    try:
        client.cancelGroupInvitation(op.param1,[op.param3])
    except Exception as e:
        print e
        print ("\n\nCANCEL_INVITATION_GROUP\n\n")
        return

tracer.addOpInterrupt(31,CANCEL_INVITATION_GROUP)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "Mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "Me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                if msg.text == "Gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "Mid:":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "Gid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "Info Bot":
                    sendMessage(msg.to,"Ini adalah Vodka,Diedit oleh Satria")
                if msg.text == "Ginfo":
                    group = client.getGroup(msg.to)
                    md = "[Group Name]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[Group Picture]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nInvitationURL: Permitted\n"
                    else: md += "\n\nInvitationURL: Refusing\n"
                    if group.invitee is None: md += "\nMembers: " + str(len(group.members)) + "人\n\nInviting: 0People"
                    else: md += "\nMembers: " + str(len(group.members)) + "People\nInvited: " + str(len(group.invitee)) + "People"
                    sendMessage(msg.to,md)
                if "Gn " in msg.text:
                    key = msg.text[22:]
                    group = client.getGroup(msg.to)
                    group.name = key
                    client.updateGroup(group)
                    sendMessage(msg.to,"Group Name"+key+"Changed to")
                if msg.text == "Url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "Open":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "Sudah dibuka")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "......dibuka")
                if msg.text == "Close":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "Sudah ditutup")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "....ditutup")
                if "Kick:" in msg.text:
                    key = msg.text[5:]
                    client.kickoutFromGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"Maaf,anda saya kick :((")
                if "Kick " in msg.text:
                    key = msg.text[3:]
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    if key in Names:
                        kazu = Names.index(key)
                        sendMessage(msg.to, "Selamat tinggal,maaf saya kick.jika saya kick berarti anda memiliki kesalahan")
                        client.kickoutFromGroup(msg.to, [""+Mids[kazu]+""])
                        contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to, ""+contact.displayName+" <~~ Maafkan")
                    else:
                        sendMessage(msg.to, "Fail")
                if msg.text == "Cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "Gaada yang menginvite.")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " Done")
                if "Invite:" in msg.text:
                    key = msg.text[-33:]
                    client.findAndAddContactsByMid(key)
                    client.inviteIntoGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+" Saya Invite kamu")
                if msg.text == "Saya":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if "Show:" in msg.text:
                    key = msg.text[-33:]
                    sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"'s contact")
                if msg.text == "Waktu":
                    sendMessage(msg.to, "Current time is" + datetime.datetime.today().strftime('_%Y_%m_%d_ %H:%M:%S') + "is")
                if msg.text == "Unicode":
                    sendMessage(msg.to,"Unicode by line.me/ti/p/~satria_hk     ITS Loading.........")
                    sendMessage(msg.to,"0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.0.04.")
                    sendMessage(msg.to,"Unicode is Finish")






































#-------------------------------------------------------------
		if msg.text == "Speed":
                    start = time.time()
                    elapsed_time = time.time() - start
                    sendMessage(msg.to, "%sseconds" % (elapsed_time))
                    print ("\nCek Speed Bot")

                if msg.text == "Tagall":
		      group = client.getGroup(msg.to)
		      mem = [contact.mid for contact in group.members]
		      for mm in mem:
		       xname = client.getContact(mm).displayName
		       xlen = str(len(xname)+1)
		       msg.contentType = 0
                       msg.text = "@"+xname+" "
		       msg.contentMetadata ={'MENTION':'{"MENTIONEES":[{"S":"0","E":'+json.dumps(xlen)+',"M":'+json.dumps(mm)+'}]}','EMTVER':'4'}
		       try:
                         client.sendMessage(msg)
		       except Exception as error:
                   	 print error
                if msg.text == "Spam":
                    sendMessage(msg.to,"GROUP HAS BEEN SPAMMED,SPAM START")
                    sendMessage(msg.to,"1")
                    sendMessage(msg.to,"2")
                    sendMessage(msg.to,"3")
                    sendMessage(msg.to,"BOOM BITCH!")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh") 
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh") 
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh") 
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"hedhhdhdhdhdhdgdbgrevdvdhdhshshshshshsh")
                    sendMessage(msg.to,"SPAM IS DONE")
                    sendMessage(msg.to,"Thx for use our service,Mister Satria")
                if msg.text == "welcome":
                    sendMessage(msg.to,"Selamat datang di grup ini,Semoga betah selalu dan jangan lupa untuk menjaga sopan santun kamu.  kenalkan nama saya Satria 😆")

                if msg.text == "Kick+":
                    print "ok"
                    _name = msg.text.replace("Kick+","")
                    gs = client.getGroup(msg.to)
                    sendMessage(msg.to,"Kick+ by hanskills")
                    sendMessage(msg.to,"Kick+ Starting")
                    sendMessage(msg.to,"Progress.....")
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        sendMessage(msg.to,"Not found.")
                        sendMessage(msg.to,"Not found.")
                        sendMessage(msg.to,"Not found.")
                    else:
                        for target in targets:
                            try:
                                klist=[client]
                                kicker=random.choice(klist)
                                kicker.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                sendText(msg.to,"Group cleanse")
                                sendText(msg.to,"Group cleanse")
                                sendText(msg.to,"Group cleanse")
                if msg.text == "Gft":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "Poin":
                    sendMessage(msg.to, "Dev,ini point read kamu♪\n「baca」<kalo mau tau yang baca♪,Biar tau siders aneh :v")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "Populer":
                    sendMessage(msg.to,"Sekarang bot sedang populer")
                if msg.text == "Karie":
                    sendMessage(msg.to,"Karie jelek,banyakan micin minta ditampol")
                if msg.text == "Baca":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "Daftar yang baca %s\n^\n\nYang jadi sider\n%sSiders Abnormal♪\n\nPoint baca dibuat:\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "Belom di set.\n「poin」ketik poin dahulu♪")
                else:
                    pass
        else:
            pass

    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
