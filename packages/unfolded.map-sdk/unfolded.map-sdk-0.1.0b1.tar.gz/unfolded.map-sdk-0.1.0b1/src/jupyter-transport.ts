import { UnfoldedMapModel } from './widget-model';

export interface Message {
  messageId: string;
  type: string;
  data: object;
}

export default class JupyterTransport {
  private readonly model: UnfoldedMapModel;
  private readonly queue: Array<Message> = new Array<Message>();
  private mapReady: boolean = false;
  private destroyed: boolean = false;

  constructor(model: UnfoldedMapModel) {
    this.model = model;
    this.model.on('msg:custom', this.messageReceived);
    this.model.listenTo(this.model, 'destroy', this.finalize);
  }

  setMapReady(value: boolean) {
    console.log('setMapReady', value, this.queue.length);
    this.mapReady = value;
    if (this.mapReady) {
      let msg;
      while ((msg = this.queue.shift()) !== undefined) {
        this.sendMessageToMapSDK(msg);
      }
    }
  }

  protected finalize = () => {
    this.destroyed = true;
    this.model.off('msg:custom', this.messageReceived);
    this.model.stopListening(this.model, 'destroy', this.finalize);
  };

  /**
   * Forwards messages received from Jupyter to Map SDK
   * @param message
   * @param buffers
   */
  protected messageReceived = (
    message: Message,
    buffers?: ArrayBuffer[] | ArrayBufferView[]
  ) => {
    if (this.destroyed) return;
    console.log('messageReceived', message);

    if (this.mapReady) {
      this.sendMessageToMapSDK(message);
    } else {
      // Keep messages in the queue for until map is ready
      this.queue.push(message);
    }
  };

  protected sendMessageToMapSDK(message: Message) {
    const { messageId, type, data } = message;
    const map = this.model.get('map');
    map
      .sendMessage(type, data)
      .then((result: object) => this.sendResponseToJupyter(messageId, result));
  }

  /**
   * Back-channel messaging: sending responses from Map SDK to Jupyter
   * @param result
   */
  protected sendResponseToJupyter = (messageId: string, data: object) => {
    if (this.destroyed) return;
    const response = { messageId, data };
    console.log('sendResponse', response);
    this.model.send(response, []);
  };
}
