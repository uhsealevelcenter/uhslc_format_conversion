import geojson

with open('meta.geojson') as f:
    gj = geojson.load(f)
features = gj['features']

features_tg_viewer = []
for feature in features:
    if feature.geometry.coordinates[0] > 180:
        feature.geometry.coordinates[0] = feature.geometry.coordinates[0] - 360
    features_tg_viewer.append(feature)

feature_collection = geojson.FeatureCollection(features_tg_viewer)
with open('meta_tg_viewer.geojson', 'w') as f:
    geojson.dump(feature_collection, f)
