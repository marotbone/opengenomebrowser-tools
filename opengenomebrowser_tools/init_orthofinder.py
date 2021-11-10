import os
from .folder_looper import FolderLooper


def init_orthofinder(database_dir: str = None, skip_ignored: bool = True, sanity_check: bool = True, representatives_only: bool = False):
    if database_dir is None:
        assert 'GENOMIC_DATABASE' in os.environ, f'Cannot find the database. Please set --database_dir or environment variable GENOMIC_DATABASE'
        database_dir = os.environ['GENOMIC_DATABASE']

    orthofinder_dir = os.path.join(database_dir, 'OrthoFinder')
    fasta_dir = os.path.join(orthofinder_dir, 'fastas')

    if not os.path.isdir(orthofinder_dir):
        os.makedirs(orthofinder_dir)

    assert len(os.listdir(orthofinder_dir)) == 0, f'Error: {orthofinder_dir=} is not empty!'

    os.makedirs(fasta_dir)

    folder_looper = FolderLooper(database_dir)

    n_faas = 0
    print(f'Linking protein fastas to {fasta_dir}/{{identifier}}.faa')
    for genome in folder_looper.genomes(skip_ignored=skip_ignored, sanity_check=sanity_check, representatives_only=representatives_only):
        faa_path = f"{genome.path}/{genome.get_json_attr('cds_tool_faa_file')}"
        assert os.path.isfile(faa_path), faa_path
        rel_path = os.path.relpath(faa_path, start=fasta_dir)
        os.symlink(src=rel_path, dst=f'{fasta_dir}/{genome.identifier}.faa')
        n_faas += 1

    cmd = f'orthofinder -f {fasta_dir}'
    container_cmd = f'-it --rm -v {database_dir}:/input:Z davidemms/orthofinder orthofinder -f /input/OrthoFinder/fastas'
    podman_cmd = f'podman run --ulimit=host {container_cmd}'
    docker_cmd = f'docker run --ulimit nofile=1000000:1000000 {container_cmd}'

    print(
        f'Done: Found {n_faas} faas.',
        f'',
        f'Ways to run OrthoFinder:',
        f'1) local install:',
        f'    {cmd}',
        f'',
        f'2) using podman:',
        f'    {podman_cmd}',
        f'',
        f'2) using docker:',
        f'    {docker_cmd}',
        f'',
        f'If you have many genomes, consider run OrthoFinder with the -og option.',
        f'Be sure to to use the -a and -t options!',
        f'More info on https://github.com/davidemms/OrthoFinder',
        sep='\n'
    )


def main():
    import fire

    fire.Fire(init_orthofinder)


if __name__ == '__main__':
    main()
