import { DOMWidgetModel, ISerializers } from '@jupyter-widgets/base';
import { MODULE_NAME, MODULE_VERSION } from './version';
import JupyterTransport from './jupyter-transport';

export class UnfoldedMapModel extends DOMWidgetModel {
  transport = new JupyterTransport(this);

  defaults() {
    return {
      ...super.defaults(),
      _model_name: UnfoldedMapModel.model_name,
      _model_module: UnfoldedMapModel.model_module,
      _model_module_version: UnfoldedMapModel.model_module_version,
      _view_name: UnfoldedMapModel.view_name,
      _view_module: UnfoldedMapModel.view_module,
      _view_module_version: UnfoldedMapModel.view_module_version,
      map: null
    };
  }

  onMapLoaded = () => {
    this.transport.setMapReady(true);
  };

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers
    // Add any extra serializers here
    // data_buffer: {deserialize: deserializeMatrix}
  };

  static model_name = 'UnfoldedMapModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'UnfoldedMapView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}
