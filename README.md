manifeisty: IIIF Presentation manifest creation for EmbARK
===========================================================================

`manifeisty` creates IIIF Presentation manifests using [EmbARK Web Kiosk templates](https://github.com/ColbyMuseum/embark-templates) and the [`iiif_prezi`](https://github.com/iiif-prezi/iiif-prezi) library for Python. It takes an input JSON structure containing object IDs and image info, queries embark for the IIIF manifest, corrects canvas image heights where needed, and deploys manifests of objects to a directory. Optionally, it logs any errors with the Image API-conforming server, invalid manifest formats, and web kiosk.

At Colby College Museum of Art, we use this tool to deploy the IIIF data in our [collection manifest](https://iiif.museum.colby.edu/presentation/collection/top.json).