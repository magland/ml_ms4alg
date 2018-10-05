from .ms4alg import MountainSort4
import tempfile
import shutil
import spikeinterface as si
import numpy as np

def mountainsort4(*,recording,detect_sign,clip_size=50,adjacency_radius=-1,detect_threshold=3,detect_interval=10):
  MS4=MountainSort4()
  MS4.setRecording(recording)
  geom=_get_geom_from_recording(recording)
  MS4.setGeom(geom)
  MS4.setSortingOpts(
    clip_size=clip_size,
    adjacency_radius=adjacency_radius,
    detect_sign=detect_sign,
    detect_interval=detect_interval,
    detect_threshold=detect_threshold
  )
  tmpdir = tempfile.mkdtemp()
  MS4.setNumWorkers(1)
  print('Using tmpdir: '+tmpdir)
  MS4.setTemporaryDirectory(tmpdir)
  try:
    MS4.sort()
  except:
    print('Cleaning tmpdir: '+tmpdir)
    shutil.rmtree(tmpdir)
    raise
  print('Cleaning tmpdir: '+tmpdir)
  shutil.rmtree(tmpdir)
  times,labels,channels=MS4.eventTimesLabelsChannels()
  output=si.NumpySortingExtractor()
  output.setTimesLabels(times=times,labels=labels)
  return output


def _get_geom_from_recording(recording):
  M=recording.getNumChannels()
  info0=recording.getChannelInfo(channel_id=0)
  nd=len(info0['location'])
  geom=np.zeros((M,nd))
  for i in range(M):
    info0=recording.getChannelInfo(channel_id=i)
    loc0=info0['location']
    geom[i,:]=loc0
  return geom