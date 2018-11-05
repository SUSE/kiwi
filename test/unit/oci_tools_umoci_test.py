from mock import (
    Mock, patch, call
)

from kiwi.oci_tools.umoci import OCIUmoci


class TestOCIBase(object):
    @patch('kiwi.oci_tools.base.mkdtemp')
    def setup(self, mock_mkdtemp):
        mock_mkdtemp.return_value = 'tmpdir'
        self.oci = OCIUmoci('tag')

    @patch('kiwi.oci_tools.umoci.Command.run')
    def test_init_layout(self, mock_Command_run):
        self.oci.init_layout()
        assert mock_Command_run.call_args_list == [
            call(['umoci', 'init', '--layout', 'tmpdir/oci_layout']),
            call(['umoci', 'new', '--image', 'tmpdir/oci_layout:tag'])
        ]

    @patch('kiwi.oci_tools.umoci.Command.run')
    def test_init_layout_base_image(self, mock_Command_run):
        self.oci.init_layout(True)
        mock_Command_run.assert_called_once_with(
            [
                'umoci', 'config', '--image',
                'tmpdir/oci_layout:base_layer', '--tag', 'tag'
            ]
        )

    @patch('kiwi.oci_tools.umoci.Command.run')
    def test_unpack(self, mock_Command_run):
        self.oci.unpack('dir')
        mock_Command_run.assert_called_once_with(
            ['umoci', 'unpack', '--image', 'tmpdir/oci_layout:tag', 'dir']
        )

    @patch('kiwi.oci_tools.umoci.Command.run')
    def test_repack(self, mock_Command_run):
        self.oci.repack('dir')
        mock_Command_run.assert_called_once_with(
            ['umoci', 'repack', '--image', 'tmpdir/oci_layout:tag', 'dir']
        )

    @patch('kiwi.oci_tools.umoci.Command.run')
    def test_add_tag(self, mock_Command_run):
        self.oci.add_tag('other_tag')
        mock_Command_run.assert_called_once_with(
            [
                'umoci', 'config', '--image', 'tmpdir/oci_layout:tag',
                '--tag', 'other_tag'
            ]
        )

    @patch('kiwi.oci_tools.umoci.Command.run')
    @patch('kiwi.oci_tools.umoci.datetime')
    def test_set_config(self, mock_datetime, mock_Command_run):
        strftime = Mock()
        strftime.strftime = Mock(return_value='current_date')
        mock_datetime.utcnow = Mock(
            return_value=strftime
        )
        self.oci.set_config(['data'])
        mock_Command_run.assert_called_once_with(
            [
                'umoci', 'config', 'data', '--image', 'tmpdir/oci_layout:tag',
                '--created', 'current_date'
            ]
        )

    @patch('kiwi.oci_tools.umoci.Command.run')
    def test_garbage_collect(self, mock_Command_run):
        self.oci.garbage_collect()
        mock_Command_run.assert_called_once_with(
            ['umoci', 'gc', '--layout', 'tmpdir/oci_layout']
        )