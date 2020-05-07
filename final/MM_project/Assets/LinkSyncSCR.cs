using UnityEngine;
using System.Collections;
using System.Runtime.InteropServices;
using SharpConnect;
using System.Security.Permissions;

//this script is based on the class Connector from Assests/Plugins/SharpConnect.cs
//it reads the string message from the TCP server at the IP address and port spcified


public class LinkSyncSCR : MonoBehaviour
{
    public Connector test = new Connector();
    [SerializeField] string IPaddress = "localhost";
    [SerializeField] int portNum = 6340;

    //global variables can be accessed by any class
    public static string base_x;
    public static string base_z;
    public static string base_rot;
    public static string j1;
    public static string j2;
    public static string j3;
    public static string j4;
    public static string cap;


    void Start()
    {
        print("starting Ethernet connection");
        Debug.Log(test.fnConnectResult(IPaddress, portNum, System.Environment.MachineName));
        if (test.res != "")
        {
            Debug.Log(test.res);
        }

    }

    void Update()
    {
        //print(test.strMessage);
        ProcessString();
    }

    void ProcessString()
    {
        try
        {
            string mystring = test.strMessage;
            //Debug.Log(mystring);

            if (mystring == "none   ")
            {
                Debug.Log(mystring);
            }
            else
            {
                //logging.saveencoder(mystring);
                string[] substrings = mystring.Split(',');

                base_x = substrings[0];
                base_z = substrings[1];
                base_rot = substrings[2];
                j1 = substrings[3];
                j2 = substrings[4];
                j3 = substrings[5];
                j4 = substrings[6];
                cap = substrings[7];
            }



            //for (int i = 0; i < subStrings.Length; i++)
            //{
            //    switch (subStrings[i])
            //    {
            //        case "1":
            //            //Aux position global
            //            auxPos = subStrings[i + 1];
            //            break;
            //        case "2":
            //            //main position global
            //            mainPos = subStrings[i + 1];
            //            break;
            //        case "3":
            //            //boom position global
            //            boomPos = subStrings[i + 1];
            //            break;
            //        case "4":
            //            //Boom Radius? Boom Angle?
            //            boomRad = subStrings[i + 1];
            //            break;
            //        case "5":
            //            //Slew Angle
            //            slewAngle = subStrings[i + 1];
            //            break;
            //        case "6":
            //            //boom angle
            //            boomAngle = subStrings[i + 1];
            //            break;
            //        case "7":
            //            boomRope = subStrings[i + 1];
            //            break;
            //   }
            //}
        }
        catch
        {
            print("error");
        }
        
    }

    void OnApplicationQuit()
    {
        try { test.fnDisconnect(); }
        catch { }
    }
}
