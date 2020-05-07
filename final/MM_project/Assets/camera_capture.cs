using System.IO;
using UnityEngine;

public class camera_capture : MonoBehaviour
{

    public int FileCounter = 0;
    bool cap_bool;


    private void LateUpdate()
    {
        string cap_str = LinkSyncSCR.cap;
        bool.TryParse(cap_str, out cap_bool);

        if (cap_bool)
        {
            CamCapture();
        }

        if (Input.GetKeyDown(KeyCode.Space))
        {
            CamCapture();
        }
    }

    void CamCapture()
    {
        Camera Cam = GameObject.Find("Camera_EE").GetComponent<Camera>();

        RenderTexture currentRT = RenderTexture.active;
        RenderTexture.active = Cam.targetTexture;

        Cam.Render();

        Texture2D Image = new Texture2D(Cam.targetTexture.width, Cam.targetTexture.height);
        Image.ReadPixels(new Rect(0, 0, Cam.targetTexture.width, Cam.targetTexture.height), 0, 0);
        Image.Apply();
        RenderTexture.active = currentRT;

        var Bytes = Image.EncodeToPNG();
        Destroy(Image);

        File.WriteAllBytes(Application.dataPath + "/../../images/" + FileCounter + ".png", Bytes);
        FileCounter++;
    }

}


