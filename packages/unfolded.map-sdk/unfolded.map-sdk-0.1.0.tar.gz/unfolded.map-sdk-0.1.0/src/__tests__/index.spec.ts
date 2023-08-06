// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Add any needed widget imports here (or from controls)
// import {} from '@jupyter-widgets/base';

import { createTestModel } from './utils';

import { UnfoldedMapModel } from '..';

describe('UnfoldedMap', () => {
  describe('UnfoldedMapModel', () => {
    it('should be createable', () => {
      const model = createTestModel(UnfoldedMapModel);
      expect(model).toBeInstanceOf(UnfoldedMapModel);
    });
    it('should send messages once map is ready', () => {
      const model = createTestModel(UnfoldedMapModel);
      let sent = 0;
      model.set('map', {
        sendMessage: (type: string, data: any) =>
          new Promise(resolve => {
            sent++;
            resolve({ type, data });
          })
      });
      model.trigger('msg:custom', {
        type: 'test',
        messageId: '123',
        data: { hello: 'world' }
      });
      expect(sent).toEqual(0);
      model.trigger('msg:custom', {
        type: 'test',
        messageId: '124',
        data: { hello: 'world' }
      });
      expect(sent).toEqual(0);
      model.onMapLoaded();
      expect(sent).toEqual(2);
    });
  });
});
