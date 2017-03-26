project('Meson documentation', 'c', version: '1.0')

hotdoc = find_program('hotdoc')

custom_target('doc',
    output: 'built_doc',
    command: [
        'hotdoc', 'conf', '--output', 'built_doc',
        '--include-paths', meson.current_source_dir(),
        '--project-name', meson.project_name(),
        '--project-version', meson.project_version(),
        '--sitemap', join_paths(meson.current_source_dir(), 'sitemap.txt'),
        '--html-extra-theme', join_paths(meson.current_source_dir(), 'theme/extra/'),
        '--extra-assets', join_paths(meson.current_source_dir(), 'theme/extra/images/'),
        '--disable-incremental-build', '--output-conf-file', meson.current_source_dir() + '/hotdoc.json'
    ],
    build_always: true
)
