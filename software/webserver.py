import SimpleHTTPServer
import SocketServer
import StringIO
import adc_reader
import numpy as np
from scipy.io import netcdf


reader = adc_reader.ADCReader()

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        output_file = netcdf.netcdf_file('frame.nc', 'w')
        output_file.createDimension('value', None)
        cdf_data = output_file.createVariable('frame', 'f', ('value',))
        data = np.zeros(10000)
        reader.GetFrame(data)
        cdf_data[:] = data
        output_file.close()

        f = open('frame.nc', 'r')

        # Construct a server response.
        self.send_response(200)
        self.send_header('Content-Disposition', 'attachment; filename=frame.nc')
        self.send_header('Content-type', 'application/octet-stream')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
        return


print('Server listening on port 8000...')
httpd = SocketServer.TCPServer(('', 8000), Handler)
httpd.serve_forever()
