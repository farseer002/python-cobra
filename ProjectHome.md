Python, like Java and C#, is based on a stack-based virtual machine. It will be very existing if you can "see" the execution flow of the Python's vm. Cobra is such a project that visualize the vm. In Cobra, you can see how many bytecodes will be executed by the vm for a Python statement, you can see how a bytecode affecting the namespace and vm's stack.Understanding the mechanism of the vm will improve your understanding of Python.

The Cobra is made up by three main componenets: VM Server, Web Server and Web Client. I use Django to build web server. And in the web client, I use Ajax to communicate with web server. The web server will connect to the vm server to get information after it received the command from web client. The vm server is modified from Python itself. So here is the simplest architecture.

<br />
Browser <---- ajax ----> Web Server(Django) <---- socket ----> VM Server(Modified Pythonn)