""" The various actions for the Scene plugin. """


# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005-2007, Enthought, Inc.
# License: BSD Style.


# Enthought library imports.
from enthought.pyface.api import FileDialog, OK
from enthought.pyface.action.api import Action
from enthought.traits.api import Str


def get_scene_manager(window):
    """ Return the scene manager for a given workbench window. """

    scene_manager = window.application.get_service(
        'enthought.tvtk.plugins_e3.scene.scene_manager.SceneManager'
    )

    return scene_manager


class NewScene(Action):
    """ An action that creates a new TVTK scene. """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """

        from enthought.tvtk.plugins_e3.scene.scene_editor import SceneEditor

        self.window.edit(object(), kind=SceneEditor)

        return


class SaveScene(Action):
    """ An action that saves a scene to an image. """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """        

        extensions = [
            '*.png', '*.jpg', '*.jpeg', '*.tiff', '*.bmp', '*.ps', '*.eps',
            '*.tex', '*.rib', '*.wrl', '*.oogl', '*.pdf', '*.vrml', '*.obj',
            '*.iv'
        ]

        wildcard = '|'.join(extensions)

        dialog = FileDialog(
            parent   = self.window.control,
            title    = 'Save scene to image',
            action   = 'save as',
            wildcard = wildcard
        )
        if dialog.open() == OK:
            view = get_scene_manager(self.window).current_editor
            if view is not None:
                view.scene.save(dialog.path)

        return
    

class SaveSceneToImage(Action):
    """ An action that saves a scene to an image. """

    # Name of the image.
    name = Str('image')

    # The wildcard for the file dialog.
    wildcard = Str("All files (*.*)|*.*")

    # The save method name.
    save_method = Str('save')

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """        

        dialog = FileDialog(
            parent   = self.window.control,
            title    = 'Save scene to %s' % self.name,
            action   = 'save as',
            wildcard = self.wildcard
        )
        if dialog.open() == OK:
            view = get_scene_manager(self.window).current_editor
            if view is not None:
                method = getattr(view.scene, self.save_method)
                method(dialog.path)

        return


# These are all specific subclasses that save particular images.
class SaveSceneToPNG(SaveSceneToImage):
    name        = 'PNG Image'
    wildcard    = 'PNG images (*.png)|*.png|' \
                  'All files (*.*)|*.*'
    save_method = 'save_png'
    
class SaveSceneToJPEG(SaveSceneToImage):
    name        = 'JPEG Image'
    wildcard    = 'JPEG images (*.jpg)|*.jpg|' \
                  'JPEG images (*.jpeg)|*.jpeg|' \
                  'All files (*.*)|*.*'
    save_method = 'save_jpg'

class SaveSceneToBMP(SaveSceneToImage):
    name        = 'BMP Image'
    wildcard    = 'BMP images (*.bmp)|*.bmp|' \
                  'All files (*.*)|*.*'
    save_method = 'save_bmp'

class SaveSceneToTIFF(SaveSceneToImage):
    name        = 'TIFF Image'
    wildcard    = 'TIFF images (*.tif)|*.tif|' \
                  'TIFF images (*.tiff)|*.tiff|' \
                  'All files (*.*)|*.*'
    save_method = 'save_tiff'

class SaveSceneToPS(SaveSceneToImage):
    name        = 'PostScript bitmap Image'
    wildcard    = 'PostScript bitmap images (*.ps)|*.ps|' \
                  'All files (*.*)|*.*'
    save_method = 'save_ps'

class SaveSceneToGL2PS(SaveSceneToImage):
    name        = 'Vector PS/EPS/PDF/TeX'
    wildcard    = 'All files (*.*)|*.*|' \
                  'EPS files (*.eps)|*.eps|' \
                  'PS files (*.ps)|*.ps|' \
                  'PDF files (*.pdf)|*.pdf|' \
                  'TeX files (*.tex)|*.tex'
    save_method = 'save_gl2ps'

class SaveSceneToRIB(SaveSceneToImage):
    name        = 'RenderMan RIB file'
    wildcard    = 'RIB files (*.rib)|*.rib|' \
                  'All files (*.*)|*.*'
    save_method = 'save_rib'

class SaveSceneToOOGL(SaveSceneToImage):
    name        = 'GeomView OOGL file'
    wildcard    = 'OOGL files (*.oogl)|*.oogl|' \
                  'All files (*.*)|*.*'
    save_method = 'save_oogl'

class SaveSceneToIV(SaveSceneToImage):
    name        = 'OpenInventor file'
    wildcard    = 'OpenInventor files (*.iv)|*.iv|' \
                  'All files (*.*)|*.*'
    save_method = 'save_iv'

class SaveSceneToVRML(SaveSceneToImage):
    name        = 'VRML file'
    wildcard    = 'VRML files (*.wrl)|*.wrl|' \
                  'All files (*.*)|*.*'
    save_method = 'save_vrml'

class SaveSceneToOBJ(SaveSceneToImage):
    name        = 'Wavefront OBJ file'
    wildcard    = 'OBJ files (*.obj)|*.obj|' \
                  'All files (*.*)|*.*'
    save_method = 'save_wavefront'


class SetView(Action):
    """Sets the scene to a particular view."""

    # The method to invoke on the scene that will set the view.
    view_method = Str

    def perform(self, event):
        """ Performs the action. """

        view = get_scene_manager(self.window).current_editor
        if view is not None:
            method = getattr(view.scene, self.view_method)
            method()

        return
    
# These are all specific subclasses that invoke particular views.
class ResetZoom(SetView):
    view_method = 'reset_zoom'

class IsometricView(SetView):
    view_method = 'isometric_view'

class XPlusView(SetView):
    view_method = 'x_plus_view'

class XMinusView(SetView):
    view_method = 'x_minus_view'
    
class YPlusView(SetView):
    view_method = 'y_plus_view'

class YMinusView(SetView):
    view_method = 'y_minus_view'

class ZPlusView(SetView):
    view_method = 'z_plus_view'

class ZMinusView(SetView):
    view_method = 'z_minus_view'

#### EOF ######################################################################