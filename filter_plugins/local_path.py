#!/usr/bin/python3

class FilterModule:
    def filters(self):
        return {'non_local_paths': self.non_local_paths}

    def non_local_paths(self, paths) -> list[str]:
        """
        Returns all paths from a docker-paths list that refer to docker-volumes instead of local paths
        """
        correct_paths = []
        for path in paths:
            if path.startswith('.') or path.startswith('/'):
                continue
            correct_paths.append(path.split(':')[0])
        return correct_paths
