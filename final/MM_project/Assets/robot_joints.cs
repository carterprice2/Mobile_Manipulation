using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class robot_joints : MonoBehaviour
{
    // speed update for the rotation of joints
    [SerializeField] float speed = 10;
    [SerializeField] float speed_move = 2;

    GameObject J1;
    GameObject J2_mark;
    GameObject J3_mark;
    GameObject J4_mark;
    GameObject robo;


    Vector3 movementVectorX = new Vector3(1f, 0f, 0f);
    Vector3 movementVectorZ = new Vector3(0f, 0f, 1f);
    Vector3 newPos;

    float j1_ang, j2_ang, j3_ang, j4_ang;
    float pos_x, pos_z, base_ang;

    bool keyboard = false;

    // Start is called before the first frame update
    void Start()
    {
        J1 = GameObject.Find("J1");
        J2_mark = GameObject.Find("J2_mark");
        J3_mark = GameObject.Find("J3_mark");
        J4_mark = GameObject.Find("J4_mark");
        robo = GameObject.Find("Robot");
    }

    // Update is called once per frame
    void Update()
    {
        if (keyboard)
        {
            base_move();
            base_rot();
            J1_rot();
            J2_rot();
            J3_rot();
            J4_rot();
        }
        else
        {
            joint_update();
            base_update();
        }
        
        
    }

    private void base_update()
    {
        string pos_x_str = LinkSyncSCR.base_x;
        float.TryParse(pos_x_str, out pos_x);
        string pos_z_str = LinkSyncSCR.base_z;
        float.TryParse(pos_z_str, out pos_z);
        transform.localPosition = new Vector3(pos_x, transform.localPosition.y, pos_z);

        string ang_str = LinkSyncSCR.base_rot;
        float base_ang_prev = base_ang;
        float.TryParse(ang_str, out base_ang);
        transform.localRotation = Quaternion.Euler(transform.eulerAngles.x, base_ang-base_ang_prev, transform.eulerAngles.z);
    }

    private void joint_update()
    {
        string ang_str = LinkSyncSCR.j1;
        float j1_ang_prev = j1_ang;
        float.TryParse(ang_str, out j1_ang);
        J1.transform.localRotation = Quaternion.Euler(J1.transform.eulerAngles.x, j1_ang-j1_ang_prev, J1.transform.eulerAngles.z);

        ang_str = LinkSyncSCR.j2;
        float.TryParse(ang_str, out j2_ang);
        J2_mark.transform.localRotation = Quaternion.Euler(j2_ang, J2_mark.transform.eulerAngles.y, J2_mark.transform.eulerAngles.z);

        ang_str = LinkSyncSCR.j3;
        float.TryParse(ang_str, out j3_ang);
        J3_mark.transform.localRotation = Quaternion.Euler(j3_ang, 0, 0);

        ang_str = LinkSyncSCR.j4;
        float.TryParse(ang_str, out j4_ang);
        J4_mark.transform.localRotation = Quaternion.Euler(j4_ang, 0, 0);

        //Debug.Log("J1" + j1_ang);
        //Debug.Log("j2 " + j2_ang);
        //Debug.Log("J3 " + j3_ang);
        //Debug.Log("J4 " + j4_ang);

    }
    private void base_move()
    {
        float moveThisFrame = speed_move * Time.deltaTime;

        newPos = transform.localPosition;
        Vector3 move_z = new Vector3(0f, 0f, 0f);
        Vector3 move_x = new Vector3(0f, 0f, 0f);

        // movementVectorZ = transform.TransformDirection(transform.eulerAngles);

        if (Input.GetKey(KeyCode.UpArrow))
        {
            move_z = moveThisFrame * movementVectorZ;
            Debug.Log("move base");
        }
        else if (Input.GetKey(KeyCode.DownArrow))
        {
            move_z = - moveThisFrame * movementVectorZ;
            Debug.Log("move base" );
        }

        if (Input.GetKey(KeyCode.LeftArrow))
        {
            move_x = -moveThisFrame * movementVectorX;
            Debug.Log("move base");
        }
        else if (Input.GetKey(KeyCode.RightArrow))
        {
            move_x = moveThisFrame * movementVectorX;
            Debug.Log("move base");
        }

        transform.localPosition = newPos + move_z + move_x;
        //robo.transform.localPosition = newPos + move_z + move_x;



    }


    private void base_rot()
    {
        float rotationThisFrame = speed * Time.deltaTime;

        if (Input.GetKey(KeyCode.Q))
        {
            //transform.localRotation = Quaternion.Euler(Vector3.up * rotationThisFrame);
            transform.RotateAround(transform.localPosition, Vector3.up, rotationThisFrame);
            //robo.transform.Rotate(Vector3.up * rotationThisFrame);
            Debug.Log("Rotate base" + rotationThisFrame);
        }
        else if (Input.GetKey(KeyCode.W))
        {
            transform.RotateAround(transform.localPosition,Vector3.up, -rotationThisFrame);
            //robo.transform.Rotate(-Vector3.up * rotationThisFrame);
            Debug.Log("Rotate Base" + rotationThisFrame);
        }

    }

    private void J1_rot()
    {
        float rotationThisFrame = speed * Time.deltaTime;

        if (Input.GetKey(KeyCode.A))
        {
            J1.transform.Rotate(Vector3.up * rotationThisFrame);
            //J2_mark.transform.Rotate(Vector3.right * rotationThisFrame);
            Debug.Log("Rotate J1" + rotationThisFrame);
        }
        else if (Input.GetKey(KeyCode.S))
        {
            J1.transform.Rotate(-Vector3.up * rotationThisFrame);
            //J2_mark.transform.Rotate(-Vector3.up * rotationThisFrame);
            Debug.Log("Trying to rotate, pressing D" + rotationThisFrame);
        }

    }

    private void J2_rot()
    {
        float rotationThisFrame = speed * Time.deltaTime;

        if (Input.GetKey(KeyCode.Z))
        {
            J2_mark.transform.Rotate(Vector3.right * rotationThisFrame);
            Debug.Log("Rotate J2" + rotationThisFrame);
        }
        else if (Input.GetKey(KeyCode.X))
        {
            J2_mark.transform.Rotate(-Vector3.right * rotationThisFrame);
            Debug.Log("rotate J2" + rotationThisFrame);
        }

    }

    private void J3_rot()
    {
        float rotationThisFrame = speed * Time.deltaTime;

        if (Input.GetKey(KeyCode.O))
        {
            J3_mark.transform.Rotate(Vector3.right * rotationThisFrame);
            Debug.Log("Rotate J3" + rotationThisFrame);
        }
        else if (Input.GetKey(KeyCode.P))
        {
            J3_mark.transform.Rotate(-Vector3.right * rotationThisFrame);
            Debug.Log("rotate J3" + rotationThisFrame);
        }
    }

    private void J4_rot()
    {
        float rotationThisFrame = speed * Time.deltaTime;

        if (Input.GetKey(KeyCode.K))
        {
            J4_mark.transform.Rotate(Vector3.right * rotationThisFrame);
            Debug.Log("Rotate J3" + rotationThisFrame);
        }
        else if (Input.GetKey(KeyCode.L))
        {
            J4_mark.transform.Rotate(-Vector3.right * rotationThisFrame);
            Debug.Log("rotate J3" + rotationThisFrame);
        }
    }
}
