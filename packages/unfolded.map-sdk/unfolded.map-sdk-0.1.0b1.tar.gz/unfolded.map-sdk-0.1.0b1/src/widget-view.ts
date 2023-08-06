import { DOMWidgetView } from '@jupyter-widgets/base';

import '../css/widget.css';
import { createMap } from '@unfolded/map-sdk';
import { UnfoldedMapModel } from './widget-model';

export class UnfoldedMapView extends DOMWidgetView {
  initialize() {
    const height = this.model.get('height');
    const mapUUID = this.model.get('mapUUID');
    const mapUrl = this.model.get('mapUrl');

    const map = createMap({
      mapUUID,
      mapUrl,
      appendToDocument: false,
      // @ts-ignore
      width: '100%', // TODO: JS Map SDK doesn't yet support 100%
      height,
      embed: true,
      onLoad: (this.model as UnfoldedMapModel).onMapLoaded
    });

    // TODO: do we really need to store map in the widget model?
    this.model.set('map', map);
    this.model.save_changes();

    return map;
  }

  render() {
    this.el.classList.add('unfolded-widget');

    const map = this.model.get('map');
    const height = this.model.get('height');

    const { iframe } = map;
    iframe.setAttribute(
      'style',
      `width: 100% !important; height: ${height}px;`
    );
    this.el.appendChild(iframe);
  }
}
