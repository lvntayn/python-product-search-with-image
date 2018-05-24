import werkzeug
from flask_restful import Resource, reqparse
from profind.database.mysql import MySQL
from PIL import Image
from profind.config import Config
from profind.engine.compare import Compare
from profind.engine.deep_feature import DeepFeature


class Search(Resource):
    def post(self):
        """ Search Photo """

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('unique_id', required=True, help="Unique ID is required.")
        parser.add_argument('photo', type=werkzeug.FileStorage, location='files')
        args = parser.parse_args()
        unique_id = args['unique_id']

        """ Save Image """
        image_name = Config.search_image_path() + '/' + unique_id + '.jpg'
        if args['photo']:
            photo = args['photo']
            photo.save(image_name)

        """ Resize Image """
        try:
            im = Image.open(image_name)
            width, height = im.size
            new_width = 128
            new_height = new_width * height / width
            size = new_width, new_height
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(image_name, "JPEG")
        except:
            return {'success': False}, 400

        """ Image Engine """
        compare = Compare()
        result = compare.find(image_name, 'search', '', DeepFeature())

        """ Products """
        product_id_list = []
        for image in result:
            product_image = image['idx'].split('/')
            product_id = product_image[-1].split('.')[0]
            product_id_list.append(product_id)

        mysql = MySQL()
        image_paths = mysql.getImagePaths(False)
        products = mysql.getProducts(product_id_list)
        response = []
        for row in products:
            response.append({
                'url': row['ecommerce_url'] + '/' + row['link'],
                'image': Config.base_url() + '/' + Config.product_image_path() + '/' + image_paths[row['category_id']]
                         + '/' + str(row['id']) + '.jpg',
                'name': mysql.latinToUnicode(row['name']),
                'price': str(row['price']),
                'currency': str(row['currency']),
                'discount': str(row['discount']),
                'merchant': row['ecommerce_name'],
            })

        register = {'unique_id': args['unique_id'], 'products': response}
        return register, 201
