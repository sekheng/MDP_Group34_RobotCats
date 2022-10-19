#from simple_communicator import SimpleCommunicator
#from multi_communicator import MultiCommunicator
from task2communicator import Task2Communicator
from task2communicatorV2 import Task2CommunicatorV2

def init():
   
    '''
    simple_communication_process = SimpleCommunicator()
    simple_communication_process.start()
    
    usrinput = 0
    
    while True:
        print("1. Manual Nav 2. Autonav Obstacle 3. Exit")
        usrinput = input()
        
        if usrinput == '1':
            simple_communication_process.manual_nav()
        elif usrinput == '2':
            simple_communication_process.autonav_obstacle()
        elif usrinput == '3':
            simple_communication_process.end()
            print("Program ended")
            break
    '''
    #task 1
    #multi_communication_process = MultiCommunicator()
    #multi_communication_process.start()

    #task 2
    task2_communication_process = Task2CommunicatorV2()
    task2_communication_process.start()

if __name__ == '__main__':
    init()
