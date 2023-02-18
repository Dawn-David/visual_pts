'''
Author: LLG
Date: 2021-09-18 15:23:27
LastEditors: Lianguang Liu
LastEditTime: 2023-02-18 14:25:52
Description: file content
'''

import numpy as np
import os

from visual_pts.visual import Visual

class Point_IO(Visual):
    '''
    Note:
        Specific class for point cloud load, save and visialization.
        Inherited from Visual class.
    Input:
        "data_path": The path of point cloud, including .xyz, .txt, .asc and .off.
        "col": "Optional('height'(default) ==> color changes along z axis, 'distance' ==> color changes along x-o-y plane, 'intensity' ==> color changes along intensity)",
        "pts_size": "point size",
    '''
    
    def __init__(self, data_path, skiprows=0, strip=True, pts_size = 1, col = 'height'):
        super().__init__()
        assert data_path.split(".")[-1] in ['xyz', 'txt', 'asc', 'off'], "file could only be xyz, txt, asc or off"
        self.data_path = data_path
        self.axis_range = 1
        self.skiprows = skiprows
        self.strip = strip
        self.pts_size = pts_size
        self.col = col

    def loadmesh(self):
        fn = self.data_path
        if fn.endswith('.txt'):
            return loadtxt(fn, skiprows=self.skiprows, strip=self.strip)
        elif fn.endswith('.asc'):
            return loadasc(fn, skiprows=self.skiprows, strip=self.strip)
        elif fn.endswith('.xyz'):
            return loadxyz(fn, skiprows=self.skiprows, strip=self.strip)
        elif fn.endswith('.off'):
            return loadoff(fn)
        else:
            raise ValueError('{}: Unknown filetype'.format(fn))
    
    def savemesh(self, *data):
        fn = self.data_path
        if fn.endswith('.txt'):
            savetxt(fn, data[0])
        elif fn.endswith('.asc'):
            saveasc(fn, data[0])
        elif fn.endswith('.xyz'):
            savexyz(fn, data[0])
        elif fn.endswith('.off'):
            saveoff(fn, data[0], data[1])
        else:
            raise ValueError('{}: Unknown filetype'.format(fn))
        
    def draw_scenes(self, fig_name=None, axis_visible = True):
        '''
        Input:
            "axis_visible": Visibility of the axis.
        '''
        self.pts = self.loadmesh()
        self.pts = self.pts[:, 0:4]
        super().draw_scenes(fig_name, axis_visible)

def loadtxt(fn, delimiter=',', comments='#', skiprows=0, strip=True):
    result = []
    with open(fn, 'r') as fid:
        row = -1
        for line in fid:
            row = row + 1
            if row < skiprows:
                continue
            if strip:
                line = line.strip()
            if line.startswith(comments):
                continue

            values = np.fromstring(line, sep=delimiter, dtype=np.float32)
            result.append(values)
    return np.array(result)


def savetxt(fn, data, delimiter=','):
    np.savetxt(fn, data, delimiter=delimiter)


def loadasc(fn, delimiter=',', comments='#', skiprows=0, strip=True):
    result = []
    with open(fn, 'r') as fid:
        row = -1
        for line in fid:
            row = row + 1
            if row < skiprows:
                continue
            if strip:
                line = line.strip()
            if line.startswith(comments):
                continue

            values = np.fromstring(line, sep=delimiter, dtype=np.float32)
            result.append(values)
    return np.array(result)


def saveasc(fn, data, delimiter=','):
    np.savetxt(fn, data, delimiter=delimiter)


def loadxyz(fn, delimiter=' ', comments='#', skiprows=0, strip=True):
    result = []
    with open(fn, 'r') as fid:
        row = -1
        for line in fid:
            row = row + 1
            if row < skiprows:
                continue
            if strip:
                line = line.strip()
            if line.startswith(comments):
                continue

            values = np.fromstring(line, sep=delimiter, dtype=np.float32)
            result.append(values)
    return np.array(result)


def savexyz(fn, data, delimiter=' '):
    np.savetxt(fn, data, delimiter=delimiter)


def loadoff(fn, delimiter=' '):
    vertices = []
    faces = []
    with open(fn, 'r') as fid:
        line = fid.readline().strip()
        if line != 'OFF':
            raise ValueError('{}: {} is not a valid OFF header'.format(fn, line))
        for line in fid:
            line = line.strip()
            if line.startswith('#'):
                continue
            if len(line) <= 0:
                continue
            num_vertices, num_faces, num_edges = [int(v) for v in line.split(' ')]
            break

        for vi in range(num_vertices):
            line = fid.readline().strip()
            vertex = [float(v) for v in line.split(' ')[:3]]
            vertices.append(vertex)

        for fi in range(num_faces):
            line = fid.readline().strip()
            face = [int(v) for v in line.split(' ')[1:4]]
            faces.append(face)

    vertices = np.array(vertices)
    faces = np.array(faces)
    return vertices, faces


def saveoff(fn, vertices, faces):
    with open(fn, 'w') as fid:
        fid.write('OFF\n')
        fid.write('{} {} {}\n'.format(vertices.shape[0], faces.shape[0], 0))
        for vert in vertices:
            fid.write('{} {} {}\n'.format(vert[0], vert[1], vert[2]))
        for face in faces:
            fid.write('{} {} {} {}\n'.format(3, face[0], face[1], face[2]))
