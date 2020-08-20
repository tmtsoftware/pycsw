import sbt._

object Dependencies {

  val TestAssembly = Seq(
    CSW.`csw-framework`,
    CSW.`csw-testkit` % Test,
    Libs.`scalatest` % Test,
    Libs.`junit` % Test,
    Libs.`junit-interface` % Test
  )

  val TestHcd = Seq(
    CSW.`csw-framework`,
    CSW.`csw-testkit` % Test,
    Libs.`scalatest` % Test,
    Libs.`junit` % Test,
    Libs.`junit-interface` % Test
  )

  val TestDeploy = Seq(
    CSW.`csw-framework`,
    CSW.`csw-logging-client`,
    CSW.`csw-testkit` % Test
  )
}
