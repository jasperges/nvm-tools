# -*- coding: utf-8 -*-

import os
import logging

from mathutils import Quaternion
from mathutils import Vector
from mathutils import Color


class Camera(object):
    """A class that represents the camera from an .nvm file.

    Args:
        name (str): The name of the camera (filename).
        focal_length (float): The focal length in pixels.
        rotation (Quaternion): Quaternion rotation of the camera.
        camera_center (Vector): Center of camera in 2D (x, y).
        distortion (Vector): k1 and k2 of the camera lens distortion model.
    """

    def __init__(self, name, focal_length, rotation, camera_center, distortion):
        self.logger = logging.getLogger("Camera")
        self.name = name
        self.focal_length = focal_length
        self. rotation = rotation
        self.camera_center = camera_data
        self.distortion = distortion

    def set_rotation(self):
        """Set the rotation of the camera."""
        # TODO
        qq = sqrt(q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3])
        if qq > 0:
            qw=q[0] / qq
            qx=q[1] / qq
            qy=q[2] / qq
            qz=q[3] / qq
        else:
            qw = 1
            qx = qy = qz = 0
        m[0][0]=float_t(qw*qw + qx*qx- qz*qz- qy*qy );
        m[0][1]=float_t(2*qx*qy -2*qz*qw );
        m[0][2]=float_t(2*qy*qw + 2*qz*qx);
        m[1][0]=float_t(2*qx*qy+ 2*qw*qz);
        m[1][1]=float_t(qy*qy+ qw*qw - qz*qz- qx*qx);
        m[1][2]=float_t(2*qz*qy- 2*qx*qw);
        m[2][0]=float_t(2*qx*qz- 2*qy*qw);
        m[2][1]=float_t(2*qy*qz + 2*qw*qx );
        m[2][2]=float_t(qz*qz+ qw*qw- qy*qy- qx*qx);

    def set_center_after_rotation(self):
        """Set the camera center after rotation."""
        # TODO
        pass


class NViewMatch(object):
    """A class that represents the N-View Match from an .nvm file.

    For more information see: http://ccwu.me/vsfm/doc.html#nvm

    Args:
        nvm_filepath (str): The full path to an .nvm file.
    """

    def __init__(self, nvm_filepath):
        self.logger = logging.getLogger("NViewMatch")
        if not os.path.isfile(os.path.normpath(nvm_filepath)):
            self.logger.error("NVM file not found: %s", nvm_filepath)
            raise FileNotFoundError("NVM file not found: {0}".format(nvm_filepath))
        self.nvm_filepath = nvm_filepath
        self.camera_data = []
        self.point_data = []

    def load(self):
        """Load the nvm file. This can take some time."""
        # TODO: improve + split into separate functions
        rotation_parameter_num = 4
        format_r9t = False

        with open(self.nvm_filepath, "r") as nvm_file:
            file_header = nvm_file.readline()
            if not file_header.startswith("NVM_V3"):
                self.logger.error("Invalid file header: %", file_header)
                raise TypeError("Invalid file header: {0}".format(file_header))
            if "R9T" in file_header:
                rotation_parameter_num = 9
                format_r9t = True

            nvm_file.readline()     # Empty line
            ncam = int(nvm_file.readline())
            if ncam <= 1:
                self.logger.warning("No cameras found.")
                return
            for i in range(ncam):
                camera_info = nvm_file.readline().split()
                token, f = camera_info[:2]
                q = camera_info[2: 2 + rotation_parameter_num]
                q = [float(i) for i in q]
                # TODO: r9t format with matrix rotation is not supported yet.
                q = Quaternion(q)
                c = camera_info[2 + rotation_parameter_num: 2 + rotation_parameter_num + 2]
                c = [float(i) for i in c]
                c = Vector(c)
                d = camera_info[2 + rotation_parameter_num + 2: 2 + rotation_parameter_num + 4]
                d = [float(i) for i in d]
                d = Vector(d)
                # TODO: investigate if a camera should be a class, so I can
                #       also create functions on it like in <util.h>
                #       SetCameraCenterAfterRotation seems like I could need it.
                camera = {
                    'name': token,
                    'focal_length': f,
                    'rotation': q,
                    'camera_center': c,
                    'distortion': d,
                    }
                self.camera_data.append(camera)
            nvm_file.readline()     # Empty line
            npoint = int(nvm_file.readline())
            if npoint <= 1:
                self.logger.warning("No 3D points found.")
                return
            for i in range(npoint):
                # TODO: for now I totally don't care about the measurements
                #       See if I need more then this.
                point_info = nvm_file.readline().split()
                pt = point_info[:3]
                pt = [float(i) for i in pt]
                pt = Vector(pt)
                cc = point_info[3:6]
                cc = [float(i) / 255 for i in cc]
                cc = Color(cc)
                point = {
                    'location': pt,
                    'color': cc,
                    }
                self.point_data.append(point)


# bool LoadNVM(ifstream& in, vector<CameraT>& camera_data, vector<Point3D>& point_data,
#               vector<Point2D>& measurements, vector<int>& ptidx, vector<int>& camidx,
#               vector<string>& names, vector<int>& ptc)
# {
#     int rotation_parameter_num = 4; 
#     bool format_r9t = false;
#     string token;
#     if(in.peek() == 'N') 
#     {
#         in >> token; //file header
#         if(strstr(token.c_str(), "R9T"))
#         {
#             rotation_parameter_num = 9;    //rotation as 3x3 matrix
#             format_r9t = true;
#         }
#     }
#     
#     int ncam = 0, npoint = 0, nproj = 0;   
#     // read # of cameras
#     in >> ncam;  if(ncam <= 1) return false; 
# 
#     //read the camera parameters
#     camera_data.resize(ncam); // allocate the camera data
#     names.resize(ncam);
#     for(int i = 0; i < ncam; ++i)
#     {
#         double f, q[9], c[3], d[2];
#         in >> token >> f ;
#         for(int j = 0; j < rotation_parameter_num; ++j) in >> q[j]; 
#         in >> c[0] >> c[1] >> c[2] >> d[0] >> d[1];
# 
#         camera_data[i].SetFocalLength(f);
#         if(format_r9t) 
#         {
#             camera_data[i].SetMatrixRotation(q);
#             camera_data[i].SetTranslation(c);
#         }
#         else
#         {
#             //older format for compability
#             camera_data[i].SetQuaternionRotation(q);        //quaternion from the file
#             camera_data[i].SetCameraCenterAfterRotation(c); //camera center from the file
#         }
#         camera_data[i].SetNormalizedMeasurementDistortion(d[0]); 
#         names[i] = token;
#     }
# 
#     //////////////////////////////////////
#     in >> npoint;   if(npoint <= 0) return false; 
# 
#     //read image projections and 3D points.
#     point_data.resize(npoint); 
#     for(int i = 0; i < npoint; ++i)
#     {
#         float pt[3]; int cc[3], npj;
#         in  >> pt[0] >> pt[1] >> pt[2] 
#             >> cc[0] >> cc[1] >> cc[2] >> npj;
#         for(int j = 0; j < npj; ++j)
#         {
#             int cidx, fidx; float imx, imy;
#             in >> cidx >> fidx >> imx >> imy;
# 
#             camidx.push_back(cidx);    //camera index
#             ptidx.push_back(i);        //point index
# 
#             //add a measurment to the vector
#             measurements.push_back(Point2D(imx, imy));
#             nproj ++;
#         }
#         point_data[i].SetPoint(pt); 
#         ptc.insert(ptc.end(), cc, cc + 3); 
#     }
#     ///////////////////////////////////////////////////////////////////////////////
#     std::cout << ncam << " cameras; " << npoint << " 3D points; " << nproj << " projections\n";
# 
#     return true;
# }
