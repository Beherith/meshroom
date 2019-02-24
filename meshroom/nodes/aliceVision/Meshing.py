__version__ = "2.0"

from meshroom.core import desc


class Meshing(desc.CommandLineNode):
    commandLine = 'aliceVision_meshing {allParams}'

    cpu = desc.Level.INTENSIVE
    ram = desc.Level.INTENSIVE

    inputs = [
        desc.File(
            name='input',
            label='Input',
            description='SfMData file.',
            value='',
            uid=[0],
        ),
        desc.File(
            name="depthMapsFolder",
            label='Depth Maps Folder',
            description='Input depth maps folder',
            value='',
            uid=[0],
        ),
        desc.File(
            name="depthMapsFilterFolder",
            label='Filtered Depth Maps Folder',
            description='Input filtered depth maps folder',
            value='',
            uid=[0],
        ),
        desc.BoolParam(
            name='estimateSpaceFromSfM',
            label='Estimate Space From SfM',
            description='Estimate the 3d space from the SfM',
            value=True,
            uid=[0],
            advanced=True,
        ),
        desc.IntParam(
            name='estimateSpaceMinObservations',
            label='Min Observations For SfM Space Estimation',
            description='Minimum number of observations for SfM space estimation.',
            value=3,
            range=(0, 100, 1),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='estimateSpaceMinObservationAngle',
            label='Min Observations Angle For SfM Space Estimation',
            description='Minimum angle between two observations for SfM space estimation. If you have many images at frequent intervals, (e.g. every 5 degrees) then set this to 4 degrees.',
            value=10,
            range=(0, 120, 1),
            uid=[0],
        ),
        desc.IntParam(
            name='maxInputPoints',
            label='Max Input Points',
            description='Max input points loaded from depth map images. This is very RAM heavy, but increasing it allows you to create very dense meshes (max 500M).',
            value=50000000,
            range=(500000, 500000000, 1000),
            uid=[0],
        ),
        desc.IntParam(
            name='maxPoints',
            label='Max Points',
            description='Max points at the end of the depth maps fusion. Go very high, 50M for super highrez meshes. Limits single block partitioning',
            value=5000000,
            range=(100000, 50000000, 1000),
            uid=[0],
        ),
        desc.IntParam(
            name='maxPointsPerVoxel',
            label='Max Points Per Voxel',
            description='Max points per voxel. Unknown if increasing or decreasing or increasing helps mesh density',
            value=1000000,
            range=(500000, 30000000, 1000),
            uid=[0],
            advanced=True,
        ),
        desc.IntParam(
            name='minStep',
            label='Min Step',
            description='The step used to load depth values from depth maps is computed from maxInputPts. '
            'Here we define the minimal value for this step, so on small datasets we will not spend '
            'too much time at the beginning loading all depth values.',
            value=2,
            range=(1, 20, 1),
            uid=[0],
            advanced=True,
        ),
        desc.ChoiceParam(
            name='partitioning',
            label='Partitioning',
            description='',
            value='singleBlock',
            values=('singleBlock', 'auto'),
            exclusive=True,
            uid=[0],
            advanced=True,
        ),
        desc.ChoiceParam(
            name='repartition',
            label='Repartition',
            description='',
            value='multiResolution',
            values=('multiResolution', 'regularGrid'),
            exclusive=True,
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='angleFactor',
            label='angleFactor',
            description='angleFactor is the max visibility angle per point',
            # https://github.com/alicevision/AliceVision/blob/d9615ca7da3fab59f3987bc9af912ee433fda732/src/aliceVision/fuseCut/DelaunayGraphCut.cpp#L1027
            #        const double angleScore = 1.0 + params.angleFactor / maxAngle;
            #       // Combine angleScore with simScore
            #       simScorePrepare[vIndex] = simScorePrepare[vIndex] * angleScore;
            value=15.0,
            range=(0.0, 200.0, 1.0),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='simFactor',
            label='simFactor',
            description='simFactor',
            value=15.0,
            range=(0.0, 200.0, 1.0),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='pixSizeMarginInitCoef',
            label='pixSizeMarginInitCoef',
            description='pixSizeMarginInitCoef, start LOW for many points, as low as 0.5',
            value=2.0,
            range=(0.0, 10.0, 0.1),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='pixSizeMarginFinalCoef',
            label='pixSizeMarginFinalCoef',
            description='pixSizeMarginFinalCoef, dont go too high with this, cause it will iteratively increase anyway (1.0 is fine)',
            value=4.0,
            range=(0.0, 10.0, 0.1),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='voteMarginFactor',
            label='voteMarginFactor',
            description='voteMarginFactor, increase to force more vertices :D',
            value=4.0,
            range=(0.1, 10.0, 0.1),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='contributeMarginFactor',
            label='contributeMarginFactor',
            description='contributeMarginFactor',
            value=2.0,
            range=(0.0, 10.0, 0.1),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='simGaussianSizeInit',
            label='simGaussianSizeInit',
            description='simGaussianSizeInit, similarity is convolved with a gaussian kernel of this size. This maybe should be reduced quite a bit for best results and to avoid smoothing',
            value=10.0,
            range=(0.0, 50.0, 0.1),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='simGaussianSize',
            label='simGaussianSize',
            description='simGaussianSize, set to lower!',
            value=10.0,
            range=(0.0, 50.0, 0.1),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='minAngleThreshold',
            label='minAngleThreshold',
            description='minAngleThreshold, if the max angle of cameras seeing this point is less than the threshold, the vertex is discarded',
            value=1.0,
            range=(0.0, 10.0, 0.01),
            uid=[0],
            advanced=True,
        ),
        desc.BoolParam(
            name='refineFuse',
            label='Refine Fuse',
            description='Refine depth map fusion with the new pixels size defined by angle and similarity scores.',
            value=True,
            uid=[0],
            advanced=True,
        ),
        desc.BoolParam(
            name='addLandmarksToTheDensePointCloud',
            label='Add Landmarks To The Dense Point Cloud',
            description='Add SfM Landmarks to the dense point cloud.',
            value=False,
            uid=[0],
            advanced=True,
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='''verbosity level (fatal, error, warning, info, debug, trace).''',
            value='info',
            values=['fatal', 'error', 'warning', 'info', 'debug', 'trace'],
            exclusive=True,
            uid=[],
        ),
    ]

    outputs = [
        desc.File(
            name="output",
            label="Output mesh",
            description="Output mesh (OBJ file format).",
            value="{cache}/{nodeType}/{uid0}/mesh.obj",
            uid=[],
            ),
        desc.File(
            name="outputDenseReconstruction",
            label="Output reconstruction",
            description="Output dense reconstruction (BIN file format).",
            value="{cache}/{nodeType}/{uid0}/denseReconstruction.bin",
            uid=[],
            group="",
            ),
    ]
