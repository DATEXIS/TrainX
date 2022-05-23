create tables:
  db.create_all()
  db.session.commit()

## Release

A new release of this software is defined by a new SemVer version number, which is set as Git tag. This triggers an automated creation of a new Docker image in the Datexis repository, which also has the version number as tag. Example:

git tag v1.0.2
git push --tags