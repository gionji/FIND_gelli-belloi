import OpenOPC
import GelliBelloi

SERVER_NAME   = 'OPC.SimaticNET'
OPC_NAME_ROOT = 'S7:[Collegamento_IM151_8]'

REGISTRO_DI_RESET_GENERALE = 'S7:[Collegamento_IM151_8]ResetAllarmi'
MACHINERY_ID  = 'gelli-belloi_01'


class OpcServer:
    def __init__(self):
        self.opc = OpenOPC.client()


    def connect(self, serverName=SERVER_NAME):
        self.serverName = serverName
        self.opc.connect( self.serverName )


    def getAvailableOpcServers(self):
        available_servers = self.opc.servers()
        return available_servers


    def __readOpcRawData(self, varGroup = GelliBelloi.VAR_GROUPS_SUPER_COMPACT):
        val = None

        try:
            val = self.opc.read( varGroup )
        except OpenOPC.TimeoutError:
            print("PLC is Off!")

        return val


    def __createJson(*elements):
        LABELS = 1
        DATA   = 0

        callerInfo = {
            "culture": "it-IT",
            "timezone": "+01:00",
            "version": "1.0.0" }

    #    output = {"machineryId": "gelli-belloi_01", "timestamp":"dd/MM/yyyy HH:mm:ss"}
        output = { "machineryId" : MACHINERY_ID }

        try:
            for couple in elements:

                if not isinstance(couple,tuple):
                    print('Problem with data: nON E UNATUPLA')
                elif not len(couple) == 2:
                    print('Problem with data: non ci sono due elementi nella tupla: ', len(couple))
                elif not len(couple[LABELS]) == len(couple[DATA]):
                    print('Problem with data: le liste non sono lunghe uguali: ', len(couple[DATA]), len(couple[LABELS]))
                    for i in range(0, max(len(couple[DATA]), len(couple[LABELS])) - 1):
                        print(i, couple[DATA][i], couple[LABELS][i])
                else:
                    # print( 'OK' )
                    output.update( dict( zip( couple[LABELS], couple[DATA] ) ) )
        except Exception as e:
            print( str(e) )
            return None

        startitJson = {'output' : output, 'callerInfo' : callerInfo}
        losantJson = output

        return startitJson, losantJson


    def getOpcDataInJsonFormats(self):
        try:
            rawDataFromOpcServer = self.__readOpcRawData()
        except:
            print("Exception occurred reading data from opc server")
            return None, None

        if rawDataFromOpcServer == None:
            print("OPC server returned no data")
            return None, None

        try:
            dataStartit, dataLosant = self.__createJson(
                    (rawDataFromOpcServer[0][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Generale] ),
                    (rawDataFromOpcServer[1][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo1.Fasi] ),
                    (rawDataFromOpcServer[2][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo1.Ingressi] ),
                    (rawDataFromOpcServer[3][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo1.Allarmi] ),
                    (rawDataFromOpcServer[4][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo2.Fasi] ),
                    (rawDataFromOpcServer[5][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo2.Ingressi] ),
                    (rawDataFromOpcServer[6][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo2.Allarmi] ),
                    (rawDataFromOpcServer[7][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo3.Fasi] ),
                    (rawDataFromOpcServer[8][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo3.Ingressi] ),
                    (rawDataFromOpcServer[9][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo3.Allarmi] )
                    )
        except:
            print("Exception occurred returning data")
            return None, None

        return dataStartit, dataLosant


    def resetAlarms():
        val = None

        try:
            val = self.opc.write( (REGISTRO_DI_RESET_GENERALE, 0x1) )
        except OpenOPC.TimeoutError:
            print("TimeoutError occured: IL PLC E SPENTO!!!")

        return val
