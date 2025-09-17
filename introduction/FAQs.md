# FAQs
Here are some frequently asked questions and direct links to the answer:

### Climate DT simulations and data:  
**Q: Which simulations are available?**   
**A:** Check out the [Climate DT simulation overview](https://destine.ecmwf.int/climate-change-adaptation-digital-twin-climate-dt/)   
**Q: Which variables were saved?**    
**A:** In [Data catalogue for ClimateDT](https://confluence.ecmwf.int/display/DDCZ/Climate+DT+Phase+1+data+catalogue#ClimateDTPhase1datacatalogue-Outputparameters) you can find an overview of the saved variables.

### Data access and download:
**Q: How can I access the Climate DT simulation data?**    
**A:** Take a look at the information in [climate_dt_data_access](climate_dt_data_access.md) and [making_a_request](./making_a_request.md).  
**Q: My download is slow, how can I speed it up?**   
**A:** You can parallelize the data access. An example is provided in [parallel_data_download.py](../example_tools/parallel_data_download.py).

### Data analysis and tools:
**Q: Where can I run my interactive analysis?**   
**A:** You can run it either in [Insula Code](https://platform.destine.eu/services/service/insula-code/) or use your local or an HPC machine which supports python/jupyter.   
**Q: Are there example notebooks for my interactive analysis?**  
**A:** Many examples are in [Polytope examples](https://github.com/destination-earth-digital-twins/polytope-examples/tree/main/climate-dt) or you can checkout the [AQUA example](../example_aqua/) or the [Cyclone detection example](../example_tropical_cyclone/).   
**Q: How do I adjust my data request?**    
**A:** You can create a request for instance by using [STAC catalogue](https://qubed.lumi.apps.dte.destination-earth.eu/) and more information in [making_a_request](making_a_request.md).   
**Q: Where can I learn about HEALPix?**     
**A:** There are multiple places to learn about HEALPix and how to process it. For instance an [introduction by easy.gems](https://easy.gems.dkrz.de/Processing/healpix/index.html) and in the Polytope resources, as well as, Earthkit.

### Documentation for software packages:
**Q: Where is the documentation for Earthkit?**   
**A:** [Earthkit docs](https://earthkit.readthedocs.io/en/latest/).   
**Q: Can I see the status of the different data-bridges somewhere?**    
Check the website [status.data.destination-earth.eu](https://status.data.destination-earth.eu/LUMI)