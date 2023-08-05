! Time-stamp: <2021-04-03 14:44:38 sander>

! create a module for python with:
! f2py -c symchaos.f90 -m symchaos_f90

MODULE symchaos

  IMPLICIT NONE
  
  ! for f2py, REAL(8) must be used instead of REAL(DP) even though DP=8
  ! https://numpy.org/devdocs/f2py/advanced.html#dealing-with-kind-specifiers
  INTEGER, PARAMETER :: DP = KIND(1.0d0)
  
CONTAINS

  SUBROUTINE calc_f90(ixres, iyres, xstart, ystart, a, b, c, d, e, n, method, &
    screen)
    INTEGER,          INTENT(IN)  :: ixres, iyres
    REAL(8),          INTENT(IN)  :: xstart, ystart, a, b, c, d, e
    INTEGER,          INTENT(IN)  :: n
    CHARACTER(LEN=*), INTENT(IN)  :: method
    INTEGER,          INTENT(OUT) :: screen(iyres, ixres)

    LOGICAL :: TRANS_SYM = .FALSE.
    REAL(8), PARAMETER :: pi = 3.14159265358979323846_DP
    INTEGER :: ix, iy, i, j
    REAL(8) :: x, y, xnew, ynew
    REAL(8) :: xoffset, xscalefactor, yoffset, yscalefactor
    REAL(8) :: xmin, xmax, ymin, ymax
    REAL(8) :: rnd
    REAL(8) :: zreal, zimag, za, zb, p ! for rot_sym

    !***************************************************************************

    CALL RANDOM_SEED()
    x = xstart
    y = ystart
    screen(:,:) = 0

    ! The range of x and y must be selected individually for each
    ! formula (method). To achieve translational symmetry, TRANS_SYM can
    ! be set to TRUE.
    SELECT CASE (TRIM(method))
    CASE ('test')
      xmin = 0.
      xmax = 1.
      ymin = 0.
      ymax = 1.
      TRANS_SYM = .TRUE.
    CASE ('clifford')
      xmin = -3.
      xmax =  3.
      ymin = -3.
      ymax =  3.
    CASE ('fern')
      xmin = -3.
      xmax =  3.
      ymin = -2.
      ymax = 12.
    CASE ('hopalong')
      x = 0. ! overwrite start value
      y = 0. ! overwrite start value
      xmin = -100.
      xmax =  100.
      ymin = -100.
      ymax =  100.
    CASE ('mondrian','quilt','quilt1','quilt2','quilt3','triangle')
      xmin = 0.
      xmax = 1.
      ymin = 0.
      ymax = 1.
      TRANS_SYM = .TRUE.
    CASE ('rot_sym')
      xmin = -1.
      xmax =  1.
      ymin = -1.
      ymax =  1.
    CASE DEFAULT
      xmin = 0.
      xmax = 1.
      ymin = 0.
      ymax = 1.
    END SELECT
    xoffset      = -xmin
    xscalefactor = 1./(xmax-xmin)
    yoffset      = -ymin
    yscalefactor = 1./(ymax-ymin)

    ! On average, the loop is executed 400 times for each pixel of the
    ! image.
    DO i = 1, 400*ixres*iyres
      
      ! see also https://en.wikipedia.org/wiki/List_of_chaotic_maps
      SELECT CASE (TRIM(method))
      CASE ('test')!qqq
        xnew = a*x + b*x * (x**2+y**2) + c*x * (x**3-3*x*y**2) + d * (x**2-y**2)
        ynew = a*y + b*y * (x**2+y**2) + c*y * (x**3-3*x*y**2) - 2*d*x*y
      CASE ('clifford')
        ! http://paulbourke.net/fractals/clifford/
        ! https://softologyblog.wordpress.com/2017/03/04/2d-strange-attractors/
        xnew = SIN(a*y) + c*COS(a*x)
        ynew = SIN(b*x) + d*COS(b*y)
      CASE ('fern')
        CALL RANDOM_NUMBER(rnd) ! 0 < rnd < 1
        ! https://en.wikipedia.org/wiki/Barnsley_fern
        IF (rnd <= 0.01) THEN ! if 0 < rnd <= 0.01
          xnew = x *   0.0   + y *   0.0   + 0.0
          ynew = x *   0.0   + y *   0.16  + 0.0
        ELSEIF (rnd <= 0.86) THEN ! if 0.01 < rnd <= 0.86
          xnew = x *   0.85  + y *   0.04  + 0.0
          ynew = x * (-0.04) + y *   0.85  + 1.6
        ELSEIF (rnd <= 0.93) THEN ! if 0.86 < rnd <= 0.93
          xnew = x *   0.2   + y * (-0.26) + 0.0
          ynew = x *   0.23  + y *   0.22  + 1.6
        ELSE ! if 0.93 < rnd < 1
          xnew = x * (-0.15) + y *   0.28  + 0.0
          ynew = x *   0.26  + y *   0.24  + 0.44
        ENDIF
      CASE ('hopalong')
        ! https://softologyblog.wordpress.com/2017/03/04/2d-strange-attractors/
        xnew = y - 1. - SQRT(ABS(b*x-1.-c)) * (x-1.) / ABS(x-1.)
        ynew = a - x - 1.
      CASE ('mondrian')
        ! These images remind me of Piet Mondrian:
        xnew = 3.*a*SIN(1/x) + 3.*b
        ynew = 3.*c*COS(1/y) + 3.*d
      CASE ('quilt')
        ! quilts from "Christmas in the House of Chaos",
        ! Scientific American, Dec 1992, JSTOR 24939340
        xnew = a*SIN(2.*pi*x) + b*SIN(2.*pi*x)*COS(2.*pi*y) &
          + c*SIN(4.*pi*x) + d*SIN(6.*pi*x)*COS(4.*pi*x) + INT(e)*x
        ynew = a*SIN(2.*pi*y) + b*SIN(2.*pi*y)*COS(2.*pi*x) &
          + c*SIN(4.*pi*y) + d*SIN(6.*pi*y)*COS(4.*pi*x) + INT(e)*y
      CASE ('quilt1')
        ! similar to "quilt" but c*COS instead of c*SIN:
        xnew = a*SIN(2.*pi*x) + b*SIN(2.*pi*x)*COS(2.*pi*y) &
          + c*COS(4.*pi*x) + d*SIN(6.*pi*y)*COS(4.*pi*x) + INT(e)*x
        ynew = a*SIN(2.*pi*y) - b*SIN(2.*pi*y)*COS(2.*pi*x) &
          + c*COS(4.*pi*y) - d*SIN(6.*pi*x)*COS(4.*pi*y) + INT(e)*y
      CASE ('quilt2')
        xnew = a*COS(2.*pi/y) + b*SIN(2.*pi*x)
        ynew = c*SIN(2.*pi/y) + d*COS(2.*pi*x)
      CASE ('quilt3')
        xnew = x**2-y**2+a*x+b*y
        ynew = 2*x*y+c*x+d*y
      CASE ('rot_sym')
        ! symmetric icon attractor with C_n symmetry
        ! Field & Golubitsky https://doi.org/10.1063/1.4822939
        ! https://softologyblog.wordpress.com/2017/03/04/2d-strange-attractors/
        zreal = x
        zimag = y
        DO j = 1, n-2 ! n=degree
          za = zreal*x - zimag*y
          zb = zimag*x + zreal*y
          zreal = za
          zimag = zb
        ENDDO
        p = a*(x**2 + y**2) + b * (x*zreal - y*zimag) + e ! e=lambda
        xnew = p*x + c*zreal - d*y
        ynew = p*y - c*zimag + d*x
      CASE ('triangle')
        xnew = a*x + b*x * (x**2+y**2) + c*x * (x**3-3*x*y**2) + d * (x**2-y**2)
        ynew = a*y + b*y * (x**2+y**2) + c*y * (x**3-3*x*y**2) - 2*d*x*y
      CASE DEFAULT
        PRINT *, "Cannot find method ", method
        STOP
      END SELECT

      ! check if the result is out of the allowed range:
      IF ((xnew<xmin).OR.(xnew>xmax).OR.(ynew<ymin).OR.(ynew>ymax)) THEN
        IF (TRANS_SYM) THEN
          ! shift it back, keeping translational symmetry:
          xnew = xnew-FLOOR(xnew)
          ynew = ynew-FLOOR(ynew)
        ELSE
          ! start with a new random value:
          CALL RANDOM_NUMBER(rnd) ! 0 < rnd < 1
          xnew = xmin + rnd * (xmax-xmin)
          CALL RANDOM_NUMBER(rnd) ! 0 < rnd < 1
          ynew = ymin + rnd * (ymax-ymin)
        ENDIF
      ENDIF

      ! transform xnew,ynew to image pixels ix,iy:
      ix = INT(ixres*(xnew+xoffset)*xscalefactor)+1
      iy = INT(iyres*(ynew+yoffset)*yscalefactor)+1
      IF (TRIM(method)=='fern') THEN
        iy = iyres-iy ! upside-down fern looks nicer if flipped
      ENDIF
      IF (i>100) THEN
        screen(iy,ix) = screen(iy,ix) + 1
      ENDIF

      x = xnew
      y = ynew

    ENDDO

    IF (TRANS_SYM) THEN
      ! make edges (more or less) seamless:
      yscalefactor = (SUM(screen(1,:)) - SUM(screen(iyres,:))) / ixres
      DO iy = 2, iyres
        screen(iy,:) = screen(iy,:) + INT((yscalefactor*(iy-1))/iyres)
      ENDDO
      xscalefactor = (SUM(screen(:,1)) - SUM(screen(:,ixres))) / iyres
      DO ix = 2, ixres
        screen(:,ix) = screen(:,ix) + INT((xscalefactor*(ix-1))/ixres)
      ENDDO
    ENDIF

  END SUBROUTINE calc_f90
  
END MODULE symchaos

!*****************************************************************************
