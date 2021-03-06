import xbmc, xbmcplugin, xbmcaddon, xbmcgui
import urllib
import resources.lib.switchking as SwitchKing
import resources.lib.utils as Utils

__addon__ = xbmcaddon.Addon(id='plugin.program.switchking')
__localize__ = __addon__.getLocalizedString
__setting__ = __addon__.getSetting

MODE_DEVICE_LIST = "devicelist"
MODE_SCENARIO_SELECT = "scenarioselect"
MODE_DEVICE_GROUP_LIST = "devicegrouplist"
MODE_DEVICE_TOGGLE_SELECT = "devicetoggleselect"
MODE_DEVICE_DIM_SELECT = "devicedimselect"

class XbmcSwitchking():

	def __init__(self):
		self.switchking = SwitchKing.SwitchKing(__setting__("host"), __setting__("port"), __setting__("username"), __setting__("password"))
		self.utils = Utils.Utils()

	def addDirectoryItem(self, name, params={}, isFolder=True, infoLabels=None):

		cm = []
		li = xbmcgui.ListItem(name)
		
		if isFolder == True:
			url = sys.argv[0] + '?' + urllib.urlencode(params)
		else:
			url = params["url"]

			if not infoLabels:
				infoLabels = { "Title": name }
			
			li.setInfo(type="executable", infoLabels=infoLabels)

		li.addContextMenuItems( cm, replaceItems=False )
			
		return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=isFolder)

	def getDeviceList(self):
		for device in self.switchking.getDevices():
			if device["dim"]:
				mode = MODE_DEVICE_DIM_SELECT
			else:
				mode = MODE_DEVICE_TOGGLE_SELECT

			self.addDirectoryItem(device["name"], { "mode": mode, "id": device["id"], "name": device["name"] })

	def scenarioSelect(self):

		scenarios = self.switchking.getScenarios()
		names = []

		for scenario in scenarios:
			names.append(scenario["name"])

		select = xbmcgui.Dialog().select(__localize__(30030), names)

		self.switchking.setScenario(scenarios[select]["id"])

		xbmcsk.getActionList()

	def deviceToggle(self, id, name):
		select = xbmcgui.Dialog().select(name, [__localize__(30010), __localize__(30011), __localize__(30012)])

		if select == 0:
			self.switchking.sendDeviceCommand(id, "turnon")

		if select == 1:
			self.switchking.sendDeviceCommand(id, "turnoff")

		if select == 2:
			self.switchking.sendDeviceCommand(id, "cancelsemiauto")

		xbmcsk.getDeviceList()

	def deviceDim(self, id, name):
		select = xbmcgui.Dialog().select(name, [__localize__(30010), __localize__(30011), __localize__(30050), __localize__(30051), __localize__(30052), __localize__(30053), __localize__(30054), __localize__(30055), __localize__(30056), __localize__(30057), __localize__(30058), __localize__(30012)])

		if select == 0:
			self.switchking.sendDeviceCommand(id, "turnon")

		if select == 1:
			self.switchking.sendDeviceCommand(id, "turnoff")

		if select == 2:
			self.switchking.sendDeviceCommand(id, "dim/10")

		if select == 3:
			self.switchking.sendDeviceCommand(id, "dim/20")

		if select == 4:
			self.switchking.sendDeviceCommand(id, "dim/30")

		if select == 5:
			self.switchking.sendDeviceCommand(id, "dim/40")

		if select == 6:
			self.switchking.sendDeviceCommand(id, "dim/50")

		if select == 7:
			self.switchking.sendDeviceCommand(id, "dim/60")

		if select == 8:
			self.switchking.sendDeviceCommand(id, "dim/70")

		if select == 9:
			self.switchking.sendDeviceCommand(id, "dim/80")

		if select == 10:
			self.switchking.sendDeviceCommand(id, "dim/90")

		if select == 11:
			self.switchking.sendDeviceCommand(id, "cancelsemiauto")
	
		xbmcsk.getDeviceList()

	def getActionList(self):
		self.addDirectoryItem(__localize__(30000), { "mode": MODE_DEVICE_LIST })
		self.addDirectoryItem(__localize__(30002), { "mode": MODE_SCENARIO_SELECT })
		#self.addDirectoryItem(__localize__(30001), { "mode": MODE_DEVICE_GROUP_LIST })

utils = Utils.Utils()	
params = utils.paramStringToDictionary(sys.argv[2])
xbmcsk = XbmcSwitchking()

mode = params.get("mode", None)
name = params.get("name", "")
id = int(params.get("id", "0"))

if len(sys.argv) < 2 or not sys.argv[2] or not mode:
	xbmcsk.getActionList()
elif mode == MODE_DEVICE_LIST:
	xbmcsk.getDeviceList()
elif mode == MODE_DEVICE_TOGGLE_SELECT and id > 0:
	xbmcsk.deviceToggle(id, name)
elif mode == MODE_DEVICE_DIM_SELECT and id > 0:
	xbmcsk.deviceDim(id, name)
elif MODE_SCENARIO_SELECT:
	xbmcsk.scenarioSelect()
else:
	print "unknown mode: " + mode
	xbmcsk.getActionList()

xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True, cacheToDisc=True)