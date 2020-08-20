import sbt._

object Libs {
  val ScalaVersion = "2.13.1"

  val `scalatest`       = "org.scalatest"          %% "scalatest"       % "3.0.8"  //Apache License 2.0
  val `scala-async`     = "org.scala-lang.modules" %% "scala-async"     % "0.10.0"  //BSD 3-clause "New" or "Revised" License
  val `junit`           = "junit"                  %  "junit"           % "4.12"   //Eclipse Public License 1.0
  val `junit-interface` = "com.novocode"           %  "junit-interface" % "0.11"   //BSD 2-clause "Simplified" License
  val `mockito-scala`   = "org.mockito"            %% "mockito-scala"   % "1.7.1"
}

object AkkaHttp {
  val Version                = "10.2.0-M1"
  val `akka-http-spray-json` = "com.typesafe.akka" %% "akka-http-spray-json" % Version
}

object CSW {
//  val Version = "2.0.1"
  val Version = "0.1.0-SNAPSHOT"

  val `csw-framework` = "com.github.tmtsoftware.csw" %% "csw-framework" % Version
  val `csw-logging-client` = "com.github.tmtsoftware.csw" %% "csw-logging-client" % Version
  val `csw-testkit`   = "com.github.tmtsoftware.csw" %% "csw-testkit" % Version
}
