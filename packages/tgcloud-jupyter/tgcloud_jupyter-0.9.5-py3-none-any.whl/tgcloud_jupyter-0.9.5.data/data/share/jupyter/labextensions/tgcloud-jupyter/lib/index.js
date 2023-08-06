import { MainAreaWidget } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { CounterWidget } from './widget';
/**
 * The command IDs used by the react-widget plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'create-react-widget';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the react-widget extension.
 */
const extension = {
    id: 'react-widget',
    autoStart: true,
    optional: [ILauncher],
    activate: (app, launcher) => {
        const { commands } = app;
        const command = CommandIDs.create;
        commands.addCommand(command, {
            caption: 'tgCloud Cloud platform',
            label: 'TigerGraph Cloud',
            iconClass: 'jp-ReactIcon',
            execute: () => {
                const content = new CounterWidget();
                const widget = new MainAreaWidget({ content });
                widget.title.label = 'TigerGraph Cloud';
                app.shell.add(widget, 'main');
            }
        });
        if (launcher) {
            launcher.add({
                command
            });
        }
    }
};
export default extension;
