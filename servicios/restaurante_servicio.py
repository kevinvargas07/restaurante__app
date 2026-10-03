    # ---------- CRUD USUARIOS ----------
    def registrar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str = "1234",
        rol: str = "Cliente"
    ) -> bool:
        """
        Registra un nuevo usuario.
        
        Returns:
            True si se registró, False si ya existe.
        Raises:
            ValueError: Si los datos son inválidos.
        """
        identificacion = identificacion.strip()
        if self.buscar_usuario(identificacion) is not None:
            return False
        
        usuario = Usuario(identificacion, nombre, correo, contrasena, rol)
        self._usuarios.append(usuario)
        self._archivo.guardar_usuarios(self._usuarios)
        return True
    
    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str = "1234",
        rol: str = "Cliente"
    ) -> bool:
        """
        Actualiza un usuario existente.
        
        Returns:
            True si se actualizó, False si no existe.
        Raises:
            ValueError: Si los datos son inválidos.
        """
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        
        # Validar los nuevos datos
        usuario_validado = Usuario(
            identificacion, nombre, correo, contrasena, rol
        )
        
        usuario.nombre = usuario_validado.nombre
        usuario.correo = usuario_validado.correo
        usuario.contrasena = usuario_validado.contrasena
        usuario.rol = usuario_validado.rol
        
        self._archivo.guardar_usuarios(self._usuarios)
        return True
    
    def eliminar_usuario(self, identificacion: str) -> bool:
        """
        Elimina un usuario por identificación.
        
        Returns:
            True si se eliminó, False si no existe.
        """
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        
        self._usuarios.remove(usuario)
        self._archivo.guardar_usuarios(self._usuarios)
        return True