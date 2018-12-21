# Heimdall
Repository about the PIBIc research project envolving the usage of low power and cost computers in parallel computing.
This is not exactly a publication because I did not have time to properly organize everything to make comprehension easier.
If you have any questions about the project please send me an email at victorcortezcb@gmail.com, I will be happy to clarify.

Brief Discription o the parts:
* Heimdall -> The basis for the distributed system. It is basically a protocol to divide tasks and give them to slave nodes who will do the heavy work.
The file "Heimdall.py" is an example applied to a biological simulation of genetic code within a population of bacteria.
* Oort -> The Heimdall protocol applied to the solution of the n-body problem in parallel. Also in the folder you can find a renderer script to render the results of the simulation.
* mergesort-> The Heimdall protocol applied to mergesort in parallel. Ginnungagap is the name of the system for this task.
* pile-> The Heimdall protocol applied to the recursive solution of the pile-splitting game in parallel
* Draugr -> It is a system for distributed file storage on the same molds of the Heimdall protocol. It divides your file into multiple chunks of defined size and each chunk carries links to the chunks before and after, essentially building a linked list. Once you have your file divided you use a central server to meet with other computers in your network and then spread your files across the network using peer-to-peer transfers. If you want to download a file you use the central servers to find who has each chunk and the client will ask other clients to download each chunk and then reconstruct the file.

The other file are just test, support or prototype files.

Feel free to explore the respository and ask me any questions.
