export default class BaseModel {
  static get VIEW_PERMISSION() {
    const { app, model } = this.contentType;
    return `${app}.view_${model}`;
  }
  static get ADD_PERMISSION() {
    const { app, model } = this.contentType;
    return `${app}.add_${model}`;
  }
  static get CHANGE_PERMISSION() {
    const { app, model } = this.contentType;
    return `${app}.change_${model}`;
  }
  static get DELETE_PERMISSION() {
    const { app, model } = this.contentType;
    return `${app}.delete_${model}`;
  }

  static itemText(item) {
    return item.name;
  }

  static get defaults() {
    return {};
  }

  constructor(data) {
    Object.assign(this, this.constructor.defaults, data);
  }
}
