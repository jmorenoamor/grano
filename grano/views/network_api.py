from flask import Blueprint, request, redirect, url_for

from grano.core import db
from grano.model import Network
from grano.validation import validate_network, ValidationContext
from grano.util import request_content, jsonify
from grano.exc import Gone, NotFound

api = Blueprint('network_api', __name__)

def _get_network(slug):
    network = Network.by_slug(slug)
    if network is None:
        raise NotFound("No such network: %s" % slug)
    return network

@api.route('/networks', methods=['GET'])
def index():
    """ List all available networks. """
    return jsonify(list(Network.all()))

@api.route('/networks', methods=['POST'])
def create():
    """ Create a new network. """
    data = request_content(request)
    context = ValidationContext()
    data = validate_network(dict(data.items()), 
            context)
    network = Network.create(data)
    db.session.commit()
    return redirect(url_for('.get', slug=network.slug))

@api.route('/networks/<slug>', methods=['GET'])
def get(slug):
    """ Get a JSON representation of the network. """
    network = _get_network(slug)
    return jsonify(network)

@api.route('/network/<slug>', methods=['PUT'])
def update(slug):
    """ Update the data of the network. """
    network = _get_network(slug)
    data = request_content(request)
    context = ValidationContext(network=network)
    data = validate_network(dict(data.items()), 
            context)
    network.update(data)
    db.session.commit()
    return jsonify(network)

@api.route('/networks/<slug>', methods=['DELETE'])
def delete(slug):
    """ Delete the resource. """
    network = _get_network(slug)
    network.delete()
    db.session.commit()
    raise Gone('Successfully deleted: %s' % slug)
