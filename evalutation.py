from profind.engine.color_feature import ColorFeature
from profind.engine.compare import Compare
from profind.engine.deep_feature import DeepFeature
from profind.engine.shape_feature import ShapeFeature
from profind.engine.texture_feature import TextureFeature

compare = Compare()
result1 = compare.find('static/search/test.jpg', 'search', '', ColorFeature())

print(result1)

result2 = compare.find('static/search/test.jpg', 'search', '', TextureFeature())

print(result2)

result3 = compare.find('static/search/test.jpg', 'search', '', ShapeFeature())

print(result3)

result4 = compare.find('static/search/test.jpg', 'search', '', DeepFeature())

print(result4)
