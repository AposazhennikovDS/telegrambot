import aiogram_calendar
import sys
import os
for path in sys.path:
   if os.path.exists(os.path.join(path, 'aiogram_calendar')):
      print('some_module is here: {}'.format(path))