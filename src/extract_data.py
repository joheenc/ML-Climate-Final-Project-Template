import os, coda
import numpy as np

for month in ['10']:
	for day in ['18','19','20','21','22','23','24','25','26','27','28','29','30','31']:#os.listdir('data/'+month):
		for filename in os.listdir('data/'+month+'/'+day):
			if filename[-3:] == '.N1':
				filehandle = coda.open('data/'+month+'/'+day+'/'+filename)
				print(f'Now reading file: data/{month}/{day}/{filename}')
				try:
					data = filehandle.fetch()
					filehandle.close()
					lats = []
					lons = []
					times = []
					for i in range(len(data.geolocation_nadir)):
						lats.append(data.geolocation_nadir[i].cen_coor_nad.latitude)
						lons.append(data.geolocation_nadir[i].cen_coor_nad.longitude)
						times.append(data.geolocation_nadir[i].dsr_time)
					datadict = data.__dict__
					for key in datadict.keys():
						if key[:4] == 'nad_':
							vcd = []
							vcd_t = []
							vcd_temp = []
							for i in range(len(datadict[key])):
								vcd.append(datadict[key][i].vcd[0])
								vcd_t.append(datadict[key][i].dsr_time)
								vcd_temp.append(datadict[key][i].temp_ref)
							vcd_lat = []
							vcd_lon = []
							for i in range(len(vcd_t)):
								idx = np.argmin(np.abs(np.array(vcd_t[i])-np.array(times)))
								vcd_lat.append(lats[idx])
								vcd_lon.append(lons[idx])
							with open(f'vcds/{key}_5.txt', 'ab') as f:
								f.write(b'\n')
								np.savetxt(f, np.vstack([np.array(vcd), np.array(vcd_t), np.array(vcd_temp), np.array(vcd_lat), np.array(vcd_lon)]))
				except:
					with open('errors.txt', 'a') as errfile:
						errfile.writelines('failed on ' + 'data/'+month+'/'+day+'/'+filename)
