# A1 for COMPSCI340/SOFTENG370 2015
# Prepared by Robert Sheehan
# Modified by Name: Shupeng Xu  UPI: sxu487   Student ID: 8260026

# You are not allowed to use any sleep calls.

import stack
import threading

from threading import Lock, Event
from process import State
from process import Type


class Dispatcher():
    """The dispatcher."""

    MAX_PROCESSES = 8

    def __init__(self):
        """Construct the dispatcher."""
        self.id = 0
        self.io_sys = None
        self.runnablelist = stack.Stack()
        self.waitinglist = []

        # for runnable stack
        self.Lock_r = threading.Lock()
        # for waiting list
        self.Lock_w = threading.Lock()
        self.stoprequest = threading.Event()
        

    def set_io_sys(self, io_sys):
        """Set the io subsystem."""
        self.io_sys = io_sys



    def dispatch_next_process(self):
        """Dispatch the process at the top of the stack."""
        self.Lock_r.acquire()
        if not self.runnablelist.isEmpty():
            process = self.runnablelist.topitem()
            self.Lock_r.release()

            process.stoprequest.set()

        else:
            self.Lock_r.release()
            return

          
    def add_process(self, process):
        """Add and start the process."""
        # add process to the top of the stack 
        """Stop currently running process first."""
        self.Lock_r.acquire()
        if not self.runnablelist.isEmpty():
            running_process = self.runnablelist.topitem()
            running_process.stoprequest.clear()


        self.runnablelist.push(process)
        process.state = State.runnable
        self.io_sys.allocate_window_to_process(process, self.runnablelist.topindex()) 
        self.Lock_r.release()

        process.start()
      
        
        
    def to_top(self, process):
        """Move the process to the top of the stack."""
        """Stop current running process first"""
        self.Lock_r.acquire()
        running_process = self.runnablelist.topitem()
        self.Lock_r.release()
        running_process.stoprequest.clear()

        self.io_sys.remove_window_from_process(process)
        self.runnablelist.remove_item(process)

        # re allocate windows according to their new position in runnable stack
        for item in self.runnablelist.items:
            self.io_sys.move_process(item, self.runnablelist.get_item_index(item))


        self.runnablelist.push(process)
        self.io_sys.allocate_window_to_process(process, self.runnablelist.topindex())
        process.stoprequest.set()



    def pause_system(self):
        """Pause the currently running process.
        As long as the dispatcher doesn't dispatch another process this
        effectively pauses the system.
        """
        self.Lock_r.acquire()
        top_p = self.runnablelist.topitem()
        self.Lock_r.release()
        top_p.stoprequest.clear()



    def resume_system(self):
        """Resume running the system."""
        self.Lock_r.acquire()
        top_p = self.runnablelist.topitem()
        self.Lock_r.release()
        top_p.stoprequest.set()



    def waiting_to_runnable(self, process):
        """Stop currently running process first."""
        self.Lock_r.acquire()
        if not self.runnablelist.isEmpty():
            running_process = self.runnablelist.topitem()
            running_process.stoprequest.clear()

        self.runnablelist.push(process)
        process.state = State.runnable
        self.io_sys.move_process(process, self.runnablelist.topindex())
        self.Lock_r.release()

        process.stoprequest.set()
        



    def wait_until_finished(self):
        """Hang around until all runnable processes are finished."""
        while True:
            """ get lock before if sentence, because proc_finish may finish process and pop the last item after the if sentence. 
            At that time, if sentence is true, but the stack is empty, so topitem will return none.
            """
            self.Lock_r.acquire()
            if not self.runnablelist.isEmpty():
                process = self.runnablelist.topitem()
                process.stoprequest.set()
                self.Lock_r.release()
            else:
                self.Lock_r.release()
                return 
        


    def proc_finished(self, process):
        """Receive notification that "proc" has finished.
        Only called from running processes.
        """
        # remove process from top of the runnable stack
        self.Lock_r.acquire()
        if(not self.runnablelist.isEmpty()):
            self.runnablelist.pop()
            self.Lock_r.release() 
            self.io_sys.remove_window_from_process(process) 
            # tell the dispatcher
            self.dispatch_next_process()

        else:
            self.Lock_r.release()
            return


    # add by Shupeng Xu, remove process from runnable stack
    def remove_process_from_runnablestack(self, process):
        # stop current running process first
        process.stoprequest.clear()

        self.Lock_r.acquire()
        self.runnablelist.remove_item(process)
        self.Lock_r.release()


    # add by Shupeng Xu, remove process from waiting stack
    def remove_process_from_waitinglist(self, process):
        
        process.stoprequest.clear()
        self.io_sys.remove_window_from_process(process)

        self.Lock_w.acquire()
        pos = self.waitinglist.index(process)
        self.waitinglist[pos] = None
        self.Lock_w.release()

        self.dispatch_next_process()



    def find_process_from_waitinglist(self, id):
        if len(self.waitinglist):
            for process in self.waitinglist:
                if not process == None:
                  if id == process.id:
                    return process

        return None



    def moveto_first_empty_position(self, process):
        for item in self.waitinglist:
            if item == None:
                old_position = self.waitinglist.index(process)
                empty_positon = self.waitinglist.index(item)
                self.waitinglist[empty_positon] = process
                self.waitinglist[old_position] = None
                return

        self.waitinglist.append(process)



    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        process.stoprequest.clear()

        self.Lock_w.acquire()
        # get the first empty position and insert the process
        if len(self.waitinglist) == 0:
            self.waitinglist.append(process)
        else:
            self.moveto_first_empty_position(process)

        self.Lock_w.release()

        self.remove_process_from_runnablestack(process)
        # change window to waiting stack
        process.state = State.waiting
        self.io_sys.move_process(process, self.waitinglist.index(process))
        self.dispatch_next_process()
           


    def runnable_process_with_id(self, id):
        """Return the runnable process with the id."""
        if(id >= 1):
            return self.runnablelist.find_item(id)


    def process_with_id(self, id):
        """Return the process with the id."""

        if(id >= 1):
            if self.runnablelist.find_item(id):
                return self.runnablelist.find_item(id)
            else: 
                return self.find_process_from_waitinglist(id)

        return None



    def kill_process(self, process):
        
        old_state = process.state
        process.state = State.killed

        if (old_state == State.runnable):
            self.runnablelist.remove_item(process)

        elif (old_state ==  State.waiting):
            position = self.waitinglist.index(process)
            self.waitinglist[position] = None

        else:
            pass

        self.io_sys.remove_window_from_process(process)
        self.dispatch_next_process()






